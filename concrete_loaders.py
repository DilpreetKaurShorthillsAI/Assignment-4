import pdfplumber
import docx
from pptx import Presentation
from file_loader import FileLoader


class PDFLoader(FileLoader):
    def validate_file(self):
        """Check if the file is a valid PDF."""
        return self.file_path.endswith('.pdf')

    def load_file(self):
        """Use pdfplumber to open and load the PDF file."""
        if not self.validate_file():
            raise ValueError("Invalid file type. Please provide a PDF file.")
        # Use pdfplumber to load the PDF
        return pdfplumber.open(self.file_path)


class DOCXLoader(FileLoader):
    def validate_file(self):
        """Check if the file is a valid DOCX file."""
        return self.file_path.endswith('.docx')

    def load_file(self):
        """Use python-docx to load the DOCX file."""
        if not self.validate_file():
            raise ValueError("Invalid file type. Please provide a DOCX file.")
        # Use python-docx to load the DOCX file
        return docx.Document(self.file_path)


class PPTLoader(FileLoader):  # Ensure this class is defined correctly
    def validate_file(self):
        """Check if the file is a valid PPTX file."""
        return self.file_path.endswith('.pptx')

    def load_file(self):
        """Use python-pptx to load the PPTX file."""
        if not self.validate_file():
            raise ValueError("Invalid file type. Please provide a PPTX file.")
        # Use python-pptx to load the PPTX file
        return Presentation(self.file_path)
