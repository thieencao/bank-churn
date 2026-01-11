import pandas as pd
import os
from etl.core.base_extractor import BaseExtractor

class BankFileExtractor(BaseExtractor):
    def __init__(self, data_path: str):
        super().__init__()
        self.data_path = data_path
        
        # --- CẤU HÌNH CHUẨN XÁC THEO FILE CỦA BẠN ---
        self.files_config = {
            # Nhóm CSV
            "churn":    {"file": "Bank_Churn.csv",   "type": "csv"},
            "customer": {"file": "CustomerInfo.csv", "type": "csv"},
            
            # Nhóm EXCEL (.xlsx)
            "geo":      {"file": "Geography.xlsx",      "type": "excel"},
            "gender":   {"file": "Gender.xlsx",         "type": "excel"},
            "active":   {"file": "ActiveCustomer.xlsx", "type": "excel"},
            "exit":     {"file": "ExitCustomer.xlsx",   "type": "excel"},
            "credit":   {"file": "CreditCard.xlsx",     "type": "excel"}
        }

    def extract(self) -> dict:
        self.logger.info(f"--- Starting Extraction from: {self.data_path} ---")
        extracted_data = {}
        
        for key, config in self.files_config.items():
            file_name = config['file']
            full_path = os.path.join(self.data_path, file_name)
            
            # 1. Kiểm tra file tồn tại
            if not os.path.exists(full_path):
                self.logger.error(f"[MISSING] File not found: {file_name}")
                continue 

            try:
                # 2. Logic đọc file theo từng loại
                if config['type'] == 'csv':
                    # CSV: Dùng read_csv
                    df = pd.read_csv(full_path, dtype=str, encoding='utf-8-sig')
                    
                elif config['type'] == 'excel':
                    # EXCEL: Dùng read_excel (engine='openpyxl')
                    # dtype=str rất quan trọng để giữ nguyên số 0 ở đầu (nếu có)
                    df = pd.read_excel(full_path, dtype=str, engine='openpyxl')
                
                else:
                    self.logger.warning(f"Unsupported type: {config['type']}")
                    continue
                
                # 3. Thêm Metadata (Tư duy chuẩn Bronze)
                df = self._add_metadata(df, file_name)
                extracted_data[key] = df
                self.logger.info(f"[OK] Extracted: {key} ({len(df)} rows)")
                
            except Exception as e:
                self.logger.error(f"[ERROR] Failed to extract {key}: {e}")
        
        return extracted_data