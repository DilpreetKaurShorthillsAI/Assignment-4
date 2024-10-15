import unittest
import os
import shutil
from extractor.data_extractor import DataExtractor
from loaders.concrete_loaders import DOCXLoader, PDFLoader, PPTLoader
from storage.concrete_storage import FileStorage, SQLStorage

class TestFileLoader(unittest.TestCase):

    def test_pdf_file_format(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        self.assertTrue(loader.validate_file())  # Check if the file is valid

    def test_docx_file_format(self):
        loader = DOCXLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/file-sample_100kB.docx')
        self.assertTrue(loader.validate_file())

    def test_ppt_file_format(self):
        loader = PPTLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/sample1.pptx')
        self.assertTrue(loader.validate_file())

    def test_file_size(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        self.assertTrue(loader.is_size_within_limit())  # Ensure this method is defined

    def test_empty_file(self):
        with open('empty.pdf', 'w') as f:
            pass
        loader = PDFLoader('empty.pdf')
        self.assertFalse(loader.validate_file())  # Should fail on empty file
        os.remove('empty.pdf')  # Cleanup

    def test_pdf_invalid_format(self):
        loader = PDFLoader('test.txt')  # Attempt to load a non-PDF file
        self.assertFalse(loader.validate_file())  # Should fail validation

    def test_corrupted_pdf_file(self):
        with open('corrupted.pdf', 'wb') as f:
            f.write(b"this is not a valid pdf")
        loader = PDFLoader('corrupted.pdf')
        self.assertFalse(loader.validate_file())  # Should fail on corrupted PDF
        os.remove('corrupted.pdf')

    def test_docx_invalid_format(self):
        loader = DOCXLoader('test.txt')  # Attempt to load a non-DOCX file
        self.assertFalse(loader.validate_file())

    def test_corrupted_docx_file(self):
        with open('corrupted.docx', 'wb') as f:
            f.write(b"this is not a valid docx")
        loader = DOCXLoader('corrupted.docx')
        self.assertFalse(loader.validate_file())  # Should fail on corrupted DOCX
        os.remove('corrupted.docx')

    def test_ppt_invalid_format(self):
        loader = PPTLoader('test.txt')  # Attempt to load a non-PPT file
        self.assertFalse(loader.validate_file())

    def test_corrupted_ppt_file(self):
        with open('corrupted.pptx', 'wb') as f:
            f.write(b"this is not a valid pptx")
        loader = PPTLoader('corrupted.pptx')
        self.assertFalse(loader.validate_file())  # Should fail on corrupted PPT
        os.remove('corrupted.pptx')

    def test_invalid_file_path(self):
        with self.assertRaises(FileNotFoundError):
            loader = PDFLoader('invalid_path.pdf')  # Path that does not exist

class TestPDFExtraction(unittest.TestCase):

    def test_pdf_text_extraction(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertIsInstance(text_data, list)
        self.assertGreater(len(text_data), 0)

    def test_pdf_image_extraction(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertIsInstance(images_data, list)
        self.assertGreater(len(images_data), 0)

    def test_pdf_link_extraction(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertIsInstance(links_data, list)
        self.assertGreater(len(links_data), 0)

    def test_pdf_table_extraction(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertIsInstance(tables_data, list)
        self.assertGreater(len(tables_data), 0)

    def test_pdf_text_extraction_empty(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertEqual(text_data, [])  # Ensure no text is extracted

    def test_pdf_link_extraction_empty(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertEqual(links_data, [])  # Ensure no links are extracted

    def test_pdf_image_extraction_empty(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertEqual(images_data, [])  # Ensure no images are extracted

    def test_pdf_table_extraction_empty(self):
        loader = PDFLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertEqual(tables_data, [])  # Ensure no tables are extracted

class TestDOCXExtraction(unittest.TestCase):

    def test_docx_text_extraction(self):
        loader = DOCXLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/file-sample_100kB.docx')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertIsInstance(text_data, list)
        self.assertGreater(len(text_data), 0)

    def test_docx_image_extraction(self):
        loader = DOCXLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/file-sample_100kB.docx')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertIsInstance(images_data, list)
        self.assertGreater(len(images_data), 0)

    def test_docx_link_extraction(self):
        loader = DOCXLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/file-sample_100kB.docx')  # Ensure this file has valid links
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertIsInstance(links_data, list)
        self.assertGreater(len(links_data), 0)

    def test_docx_table_extraction(self):
        loader = DOCXLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/file-sample_100kB.docx')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertIsInstance(tables_data, list)
        self.assertGreater(len(tables_data), 0)

    def test_docx_text_extraction_empty(self):
        loader = DOCXLoader('empty.docx')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertEqual(text_data, [])  # Ensure no text is extracted

    def test_docx_image_extraction_empty(self):
        loader = DOCXLoader('empty.docx')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertEqual(images_data, [])  # Ensure no images are extracted

    def test_docx_link_extraction_empty(self):
        loader = DOCXLoader('empty.docx')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertEqual(links_data, [])  # Ensure no links are extracted

    def test_docx_table_extraction_empty(self):
        loader = DOCXLoader('empty.docx')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertEqual(tables_data, [])  # Ensure no tables are extracted

class TestPPTExtraction(unittest.TestCase):

    def test_ppt_text_extraction(self):
        loader = PPTLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/sample1.pptx')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertIsInstance(text_data, list)
        self.assertGreater(len(text_data), 0)

    def test_ppt_image_extraction(self):
        loader = PPTLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/sample1.pptx')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertIsInstance(images_data, list)
        self.assertGreater(len(images_data), 0)

    def test_ppt_link_extraction(self):
        loader = PPTLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/sample1.pptx')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertIsInstance(links_data, list)
        self.assertGreater(len(links_data), 0)

    def test_ppt_table_extraction(self):
        loader = PPTLoader('/home/shtlp_0064/Desktop/Assignment_4 Python/samples/sample1.pptx')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertIsInstance(tables_data, list)
        self.assertGreater(len(tables_data), 0)

    def test_ppt_text_extraction_empty(self):
        loader = PPTLoader('empty.ppt')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertEqual(text_data, [])  # Ensure no text is extracted

    def test_ppt_image_extraction_empty(self):
        loader = PPTLoader('empty.ppt')
        extractor = DataExtractor(loader)
        images_data = extractor.extract_images()
        self.assertEqual(images_data, [])  # Ensure no images are extracted

    def test_ppt_link_extraction_empty(self):
        loader = PPTLoader('empty.ppt')
        extractor = DataExtractor(loader)
        links_data = extractor.extract_links()
        self.assertEqual(links_data, [])  # Ensure no links are extracted

    def test_ppt_table_extraction_empty(self):
        loader = PPTLoader('empty.ppt')
        extractor = DataExtractor(loader)
        tables_data = extractor.extract_tables()
        self.assertEqual(tables_data, [])  # Ensure no tables are extracted

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.output_directory = 'test_output_directory'
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def tearDown(self):
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

    def test_file_storage(self):
        storage = FileStorage(self.output_directory)
        text_data = ["Sample text"]
        storage.save_text_data(text_data, "test_text_data.txt")
        self.assertTrue(os.path.exists(os.path.join(self.output_directory, "test_text_data.txt")))

    def test_file_storage_with_no_data(self):
        storage = FileStorage(self.output_directory)
        storage.save_text_data([], "test_no_data.txt")  # Save empty data
        self.assertTrue(os.path.exists(os.path.join(self.output_directory, "test_no_data.txt")))

    def test_file_storage_overwrite(self):
        storage = FileStorage(self.output_directory)
        text_data = ["Sample text"]
        storage.save_text_data(text_data, "test_overwrite.txt")
        storage.save_text_data(text_data, "test_overwrite.txt")  # Overwrite
        self.assertTrue(os.path.exists(os.path.join(self.output_directory, "test_overwrite.txt")))

class TestSQLStorage(unittest.TestCase):

    def setUp(self):
        self.db_path = 'test_output.db'
        self.storage = SQLStorage(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_sql_storage(self):
        text_data = ["Sample text"]
        self.storage.save_text_data(text_data)
        # Implement a check to verify data is saved in SQL
        # You may want to implement a method to read back from the database to verify

    def test_sql_storage_empty_data(self):
        text_data = []
        self.storage.save_text_data(text_data)  # Save empty data
        # Implement a check to ensure no entry is created in the database
        # You may want to check that the count of entries is 0

    def test_sql_storage_overwrite(self):
        text_data = ["Sample text"]
        self.storage.save_text_data(text_data)
        self.storage.save_text_data(text_data)  # Overwrite previous data
        # Check to verify data is saved in SQL, ensuring it overwrites correctly
        # Implement a read-back check to ensure that the data is what you expect

    def test_close(self):
        self.storage.close()
        # Add logic to ensure the connection is indeed closed

if __name__ == '__main__':
    unittest.main()
