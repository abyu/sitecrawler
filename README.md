### Setup
  - Install python3.7
  - Run `python3.7 -m venv env` to setup a virtual enviroment
  - Run `source env/bin/activate`to activate the python virtual enviroment
  - Run `pip install --pre pybuilder`
  - Run `pyb install_dependencies` to install all project dependencies
  - Run `pyb` to run tests and create the package

### Running the app
  - `pip install crawler -e target/dist/sitecrawler-1.0.dev0/` to install package locally
  - `./run.py <url> <number_of_workers> <output_directory>` to scrape the given url
     - Scrape results get saved into a timestamped file inside the given output directory
     - Example: `./run.py https://www.webscraper.io/test-sites/e-commerce/allinone/ 20 results`
