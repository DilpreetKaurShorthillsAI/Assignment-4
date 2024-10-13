import unittest
import os
import shutil
from concrete_loaders import PDFLoader, DOCXLoader, PPTLoader
from data_extractor import DataExtractor
from concrete_storage import FileStorage, SQLStorage

class TestFileLoader(unittest.TestCase):
    
    def test_pdf_loader(self):
        # Test the PDF loader functionality
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf')
        self.assertTrue(loader.validate_file())
        content = loader.load_file()
        self.assertIsNotNone(content)


class TestDataExtractor(unittest.TestCase):
    
    def test_extract_text(self):
        # Testing text extraction functionality
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertIsInstance(text_data, list)  # Expect a list of text data

    def test_extract_links(self):
        # Test extracting links from the document
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertIsInstance(links_data, list)  # Expect a list of links

    def test_extract_images(self):
        # Test extracting images from the document
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertIsInstance(images_data, list)  # Expect a list of images

    def test_extract_tables(self):
        # Test extracting tables from the document
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertIsInstance(tables_data, list)  # Expect a list of tables


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        # Setup output directory for testing
        self.output_directory = 'test_output_directory'
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def tearDown(self):
        # Cleanup after tests: Use shutil.rmtree() to remove directories
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

    def test_save_text_data(self):
        # Test saving text data to a file
        storage = FileStorage(self.output_directory)
        text_data = ["HTML and CSS for paper-based", "Muscle"]
        storage.save_text_data(text_data, "test_text_data.csv")
        self.assertTrue(os.path.exists(os.path.join(self.output_directory, "test_text_data.csv")))

    def test_save_links_data(self):
        # Test saving links data to a file
        storage = FileStorage(self.output_directory)
        links_data = ["http://en.wikibooks.org/", "http://css4.pub"]
        storage.save_links_data(links_data, "test_links_data.csv")
        self.assertTrue(os.path.exists(os.path.join(self.output_directory, "test_links_data.csv")))



class TestSQLStorage(unittest.TestCase):

    def setUp(self):
        # Setup SQL database for testing
        self.db_path = 'test_output.db'
        self.storage = SQLStorage(self.db_path)

    def tearDown(self):
        # Cleanup SQL database after tests
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_text_data(self):
        # Test saving text data to SQL database
        text_data = ["HTML and CSS for paper-based", "Muscle"]
        self.storage.save_text_data(text_data)
        # Verify the text data is saved (You can add SQL checks to verify the entries)


    def test_save_images(self):
        # Test saving image metadata to SQL database
        images_data = []  # Assuming no actual images for this test
        self.storage.save_images(images_data)
        # Expect no data saved as images_data is empty

    def test_close(self):
        # Test closing the SQL storage connection
        self.storage.close()
        # Verify that the connection is closed without error


if __name__ == '__script__':
    unittest.main()
