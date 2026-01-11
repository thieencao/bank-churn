import pandas as pd
# Import class cha từ Core
from etl.core.base_builder import BaseBuilder

class StarSchemaBuilder(BaseBuilder): # <--- Kế thừa ở đây
    def build(self, silver_data: dict) -> dict:
        self.logger.info("--- Starting Gold Layer (Finalizing Star Schema) ---")
        
        gold_data = {}
        
        # 1. MAPPING FACT
        if 'silver_fact_churn' in silver_data:
            gold_data['fact_churn'] = silver_data['silver_fact_churn'].copy()
        else:
            self.logger.error("Missing 'silver_fact_churn'")

        # 2. MAPPING DIMS
        dim_mapping = {
            'silver_dim_geo':      'dim_geography',
            'silver_dim_gender':   'dim_gender',
            'silver_dim_customer': 'dim_customer',
            'silver_dim_active':   'dim_active_status',
            'silver_dim_exit':     'dim_exit_status',
            'silver_dim_credit':   'dim_credit_card'
        }

        for silver_name, gold_name in dim_mapping.items():
            if silver_name in silver_data:
                gold_data[gold_name] = silver_data[silver_name].copy()
                
        return gold_data