from sqlalchemy import create_engine
# Import class cha từ Core
from etl.core.base_loader import BaseLoader 

class MySQLLoader(BaseLoader): # <--- Kế thừa ở đây
    def __init__(self, connection_string: str):
        super().__init__() # Gọi logger của cha
        self.conn_str = connection_string
        try:
            self.engine = create_engine(self.conn_str)
        except Exception as e:
            self.logger.error(f"Failed to create DB engine: {e}")
            raise

    def load(self, data_dict: dict):
        self.logger.info("--- Starting Load to MySQL ---")
        
        with self.engine.begin() as conn:
            for table_name, df in data_dict.items():
                try:
                    self.logger.info(f"Loading table '{table_name}' ({len(df)} rows)...")
                    df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
                    self.logger.info(f"[SUCCESS] Loaded {table_name}")
                except Exception as e:
                    self.logger.error(f"[FAILED] Error loading {table_name}: {e}")