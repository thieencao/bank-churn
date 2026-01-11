from abc import ABC, abstractmethod
import pandas as pd
import logging

class BaseTransformer(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def cast_types(self, df: pd.DataFrame, schema: dict) -> pd.DataFrame:
        """
        Hàm ép kiểu dữ liệu an toàn.
        Ví dụ: schema = {'Age': 'numeric', 'JoinDate': 'datetime'}
        """
        df = df.copy()
        for col, dtype in schema.items():
            if col in df.columns:
                try:
                    if dtype == 'datetime':
                        # dayfirst=True quan trọng vì định dạng gốc là dd-mm-yyyy
                        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                    elif dtype == 'numeric':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    else:
                        df[col] = df[col].astype(dtype)
                except Exception as e:
                    self.logger.warning(f"Could not cast column '{col}' to {dtype}: {e}")
        return df

    def rename_cols(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        """Đổi tên cột theo dictionary"""
        return df.rename(columns=mapping)

    @abstractmethod
    def transform(self, raw_data: dict) -> pd.DataFrame:
        pass