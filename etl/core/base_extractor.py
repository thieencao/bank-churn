from abc import ABC, abstractmethod
import pandas as pd
import logging
from datetime import datetime

class BaseExtractor(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _add_metadata(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Hàm dùng chung cho tất cả các con"""
        df = df.copy()
        df['_ingested_at'] = datetime.now()
        df['_source'] = source
        return df

    @abstractmethod
    def extract(self) -> dict:
        """Các class con bắt buộc phải viết lại hàm này"""
        pass