import sys
import os
import logging

# 1. SETUP
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from etl.bronze.file_extractor import BankFileExtractor
from etl.silver.customer_transformer import SilverTransformer
from etl.gold.star_schema_builder import StarSchemaBuilder
from etl.loaders.mysql_loader import MySQLLoader

# --- CẤU HÌNH DB 
DB_CONN_STR = 'mysql+pymysql://root:123456789@localhost/bank_db'

def main():
    data_dir = os.path.join(os.getcwd(), 'data')
    
    print("==============================================")
    print("   BANK CHURN ETL: FULL PRODUCTION RUN")
    print("==============================================\n")

    # --- 1. BRONZE ---
    print(">>> STEP 1: BRONZE LAYER <<<")
    extractor = BankFileExtractor(data_dir)
    raw_data = extractor.extract()
    if not raw_data: return

    # --- 2. SILVER ---
    print("\n>>> STEP 2: SILVER LAYER <<<")
    transformer = SilverTransformer()
    silver_data = transformer.transform(raw_data)
    if not silver_data: return

    # --- 3. GOLD ---
    print("\n>>> STEP 3: GOLD LAYER (Mapping Schema) <<<")
    builder = StarSchemaBuilder()
    gold_data = builder.build(silver_data)
    
    # --- 4. LOAD ---
    print("\n>>> STEP 4: LOAD TO MYSQL <<<")
    if gold_data:
        try:
            loader = MySQLLoader(DB_CONN_STR)
            loader.load(gold_data)
            
            print("\n" + "="*50)
            print("   ✅ MISSION ACCOMPLISHED!")
            print(f"   Successfully loaded {len(gold_data)} tables to MySQL.")
            print("   You can now open Power BI and connect to 'bank_db'.")
            print("="*50)
            
        except Exception as e:
            print(f"[!] Load Error: {e}")
            print("HINT: 1. Check DB password in run_pipeline.py")
            print("      2. Ensure database 'bank_db' exists (CREATE DATABASE bank_db;)")
    else:
        print("[!] No data generated in Gold layer.")

if __name__ == "__main__":
    main()