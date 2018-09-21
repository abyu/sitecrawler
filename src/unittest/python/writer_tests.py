from unittest import TestCase
from mockito import verify, mock, patch, expect
from crawler.writer import FileWriter
import mock 

class FileWriterTest(TestCase):

  def test_create_file_with_given_data_and_file_name(self):
    filename= "sameplfile.txt"
    writer = FileWriter(filename)
    m_open = mock.mock_open()

    with mock.patch('builtins.open', m_open):
      writer.write("sometext")

    m_open.assert_called_once_with(filename, "w")
    handler = m_open()
    handler.write.assert_called_once_with("sometext")

  def test_context_data_to_string_when_persisting_to_file(self):
    filename= "sameplfile.txt"
    writer = FileWriter(filename)
    m_open = mock.mock_open()
    data = {"akey": "avalue"}

    with mock.patch('builtins.open', m_open):
      writer.write(data)

    m_open.assert_called_once_with(filename, "w")
    handler = m_open()
    handler.write.assert_called_once_with("{'akey': 'avalue'}")


