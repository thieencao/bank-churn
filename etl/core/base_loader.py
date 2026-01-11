from abc import ABC, abstractmethod
import logging

class BaseLoader(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load(self, data: dict):
        """
        Mọi Loader bắt buộc phải có hàm load.
        """
        pass