from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save_data(self, data):
        """Save extracted data to the desired storage format."""
        pass
