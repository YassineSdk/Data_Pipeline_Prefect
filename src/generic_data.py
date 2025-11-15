from prefect import flow,task 
from prefect.artifacts import create_markdown_artifact
import pandas as pd 
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import pickle
from pathlib import Path
import random
import warnings
warnings.filterwarnings('ignore')


#### data generation ####
def synthic_data(city) -> pd.DataFrame:
    nb_rows = random.randint(1,25)
    path = Path("../model/synth_model.pkl")
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")

    with open(path,'rb') as f:
        model = pickle.load(f)

    batch_data = model.sample(nb_rows)
    batch_data['agency_city'] = city
    markdown=f"""
    ### the batch size : {len(batch_data)}
    ### the columns : { batch_data.columns}
    """
    create_markdown_artifact(
        key="synthetic-data",
        markdown=markdown)

    return batch_data
