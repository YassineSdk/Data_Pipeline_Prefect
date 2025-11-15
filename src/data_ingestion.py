from prefect.artifacts import create_markdown_artifact
from prefect.cache_policies import NO_CACHE
from dotenv import load_dotenv
import pandas as pd 
import os
from sqlalchemy import create_engine,text
import warnings
warnings.filterwarnings('ignore')





#### database connection #### 
def connect_db():

    load_dotenv(dotenv_path='../.env')
    connection_str = os.getenv('connection_str')
    engine = create_engine(connection_str)
    return engine


#### ingestion of the data ####
def ingest_data(batch_data,engine,table):
    if batch_data.empty:
        raise ValueError("no data to insert")
    
    batch_data.to_sql(table, engine, if_exists="replace", index=False)
    data = pd.read_sql(f"select * from {table}",engine)
    markdown = f"""
    ####
    **preview data:** **shape** : {len(data) - len(batch_data)}
    **recent data:**  **shape** : {len(data)}
    """

    create_markdown_artifact(key="data-ingection-summary",
    markdown=markdown)