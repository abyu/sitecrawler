import logging
import multiprocessing as mp
from enum import Enum
LOGGER = logging.getLogger("crawler.parellerrunner")

class TaskAction(Enum):
  CONTINUE = 1,
  TERMINATE = 2

class ParellerRunner():

  def __init__(self, no_of_workers):
    m = mp.Manager()
    self.in_queue = m.JoinableQueue()
    self.out_queue = m.JoinableQueue()
    self.scrape_progress = m.JoinableQueue()
    self.no_of_workers = no_of_workers
    self.workers = []
    self.aggregator = None

  def setup_workers(self, target):
    workers = []
    self.worker_task = target
    for x in range(0, self.no_of_workers):
      process = mp.Process(target=self.scrape_worker, args=(self.in_queue, self.out_queue, self.scrape_progress ))
      workers.append(process)
    self.workers = workers

  def setup_aggregator(self, target, results_writer):
    self.aggregate_task = target
    self.aggregator = mp.Process(target=self.aggregate_worker, args=(self.in_queue, self.out_queue, results_writer, ))

  def start_all_jobs(self):
    LOGGER.info("Starting {0} workers".format(self.no_of_workers))
    for worker in self.workers:
      worker.start()
    if self.aggregator:
      self.aggregator.start()
    else:
      LOGGER.warning("Aggregator not started, was it set it up?")
    LOGGER.info("All jobs started")

  def wait_for_completion(self):
    while(True):
      self.in_queue.join()
      self.out_queue.join()
      LOGGER.info("Both queues are empty")
      if(self.scrape_progress.empty()):
        LOGGER.info("No more on going scrape process, terminating")
        break

  def scrape_worker(self, in_queue, out_queue, scrape_progress):
    while True:
      task_item = self.in_queue.get(True)
      url = task_item
      self.scrape_progress.put("Scrape for {0}".format(url))
      task_action = self.worker_task(url, self.out_queue)
      self.scrape_progress.get()
      self.scrape_progress.task_done()
      self.in_queue.task_done()
      if task_action == TaskAction.TERMINATE:
        LOGGER.info("TERMINATING")
        return

  def aggregate_worker(self, in_queue, out_queue, results_writer):
    visited_url = set()
    results = []
    accumulator = {'visited_url': visited_url, 'results': results}
    LOGGER.info("Aggregating")
    while True:
      task_item = out_queue.get()
      task_action, accumulator = self.aggregate_task(task_item, in_queue, accumulator)
      out_queue.task_done()
      if task_action == TaskAction.TERMINATE:
        LOGGER.info("Visited {0}".format(list(accumulator['visited_url'])))
        results_writer.write(results)
        return

  def send_term_signal_to_jobs(self):
    LOGGER.info("Sending kill signals to all workers")
    for x in range(0, self.no_of_workers):
      self.in_queue.put("TERMINATE")
    self.out_queue.put("TERMINATE")

  def wait_for_jobs_completion(self):
    self.aggregator.join()
    for worker in self.workers:
      worker.join()

  def seed_input(self, data):
    self.in_queue.put(data)

  def await_completion(self):
    self.start_all_jobs()
    self.wait_for_completion()
    self.send_term_signal_to_jobs()
    self.wait_for_jobs_completion()