from abc import ABC, abstractmethod
import logging

class BaseBuilder(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def build(self, silver_data: dict) -> dict:
        """
        Mọi Class ở tầng Gold bắt buộc phải có hàm build.
        Input: Dictionary dữ liệu từ Silver.
        Output: Dictionary dữ liệu chuẩn Gold (Fact/Dim).
        """
        pass