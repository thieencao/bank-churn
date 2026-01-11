import pandas as pd
from etl.core.base_transformer import BaseTransformer

class SilverTransformer(BaseTransformer):
    def transform(self, raw_data: dict) -> dict:
        self.logger.info("--- Starting Silver Transformation (Clean Only - No Join) ---")
        
        silver_data = {}
        
        # --- 1. XỬ LÝ BẢNG CHÍNH (FACT CHURN) ---
        if 'churn' in raw_data:
            df = raw_data['churn'].copy()
            
            # Ép kiểu dữ liệu
            schema = {
                "CreditScore": "numeric",
                "Age": "numeric",
                "Tenure": "numeric",
                "Balance": "numeric",
                "NumOfProducts": "numeric",
                "EstimatedSalary": "numeric",
                "Bank DOJ": "datetime"
            }
            df = self.cast_types(df, schema)
            
            # Feature Engineering (Tạo nhóm tuổi) - Cái này Fact nên có để phân tích nhanh
            self.logger.info("Creating Age Groups for Fact Table...")
            df = df.dropna(subset=['Age'])
            df['AgeGroup'] = pd.cut(
                df['Age'], 
                bins=[0, 30, 40, 50, 60, 150], 
                labels=['Under 30', '30-39', '40-49', '50-59', '60+']
            )
            
            # Đổi tên cột ngày tháng cho chuẩn
            df = df.rename(columns={"Bank DOJ": "JoinDate"})
            
            # QUAN TRỌNG: Loại bỏ cột RowNumber vô nghĩa, nhưng GIỮ LẠI các ID (GeographyID, GenderID...)
            # Để Power BI dùng các ID này nối với bảng Dim
            if "RowNumber" in df.columns:
                df = df.drop(columns=["RowNumber"])
                
            silver_data['silver_fact_churn'] = df
            self.logger.info(f"Processed Fact Churn: {df.shape}")

        # --- 2. XỬ LÝ CÁC BẢNG DANH MỤC (DIMENSIONS) ---
        
        # 2.1 Geography
        if 'geo' in raw_data:
            df = raw_data['geo'].copy()
            # Đổi tên cột cho dễ hiểu: GeographyLocation -> CountryName
            df = df.rename(columns={"GeographyLocation": "CountryName"})
            # Bỏ metadata thừa
            df = self._clean_metadata(df)
            silver_data['silver_dim_geo'] = df

        # 2.2 Gender
        if 'gender' in raw_data:
            df = raw_data['gender'].copy()
            # Đổi tên cột
            df = df.rename(columns={"GenderCategory": "GenderName"})
            df = self._clean_metadata(df)
            silver_data['silver_dim_gender'] = df

        # 2.3 Customer Info (Bảng Dim Khách hàng)
        if 'customer' in raw_data:
            df = raw_data['customer'].copy()
            # Bảng này nối với Fact qua CustomerId
            df = self._clean_metadata(df)
            silver_data['silver_dim_customer'] = df

        # 2.4 Active Status
        if 'active' in raw_data:
            df = raw_data['active'].copy()
            df = self._clean_metadata(df)
            silver_data['silver_dim_active'] = df

        # 2.5 Exit Status
        if 'exit' in raw_data:
            df = raw_data['exit'].copy()
            df = self._clean_metadata(df)
            silver_data['silver_dim_exit'] = df

        # 2.6 Credit Card
        if 'credit' in raw_data:
            df = raw_data['credit'].copy()
            # Đổi tên Category -> CreditCardStatus cho rõ nghĩa
            df = df.rename(columns={"Category": "CreditCardStatus"})
            df = self._clean_metadata(df)
            silver_data['silver_dim_credit'] = df

        return silver_data

    def _clean_metadata(self, df):
        """Hàm phụ: Xóa các cột metadata _ingested_at... khỏi bảng Dim cho gọn"""
        cols_to_drop = ['_ingested_at', '_source', '_source_file']
        return df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')