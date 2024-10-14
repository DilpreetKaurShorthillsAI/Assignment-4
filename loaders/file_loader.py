# file_loader.py
from abc import ABC, abstractmethod

class FileLoader(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def validate_file(self):
        """Validate that the provided file is of the correct type."""
        pass

    @abstractmethod
    def load_file(self):
        """Load the file into memory for processing."""
        pass
