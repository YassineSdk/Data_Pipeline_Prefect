
from prefect.artifacts import create_markdown_artifact
from prefect.cache_policies import NO_CACHE
import pandas as pd 
from sqlalchemy import create_engine,text
import warnings
warnings.filterwarnings('ignore')





#### Data concatination
def concatinate_data(engine):
    with engine.connect() as conn:
        conn.execute(text("""CREATE TABLE IF NOT EXISTS unified_data (
                new_price     BIGINT,
                chambres      INT,
                Sales_bain    INT,
                surface       INT,
                ascenseur     TEXT,
                floor         INT,
                terrasse      TEXT,
                parking       TEXT,
                Type          TEXT,
                City          TEXT,
                Nighberd      TEXT,
                agency_city   TEXT
            );
        """))
        data_size_1 = pd.read_sql("""select count(*) from unified_data """,engine)

        conn.execute(text("""
            INSERT INTO unified_data (
                new_price, chambres, "Sales_bain", surface,
                ascenseur, floor, terrasse, parking,
                "Type", "City", "Nighberd", agency_city
            )
            SELECT new_price, chambres, "Sales_bain", surface,
                   ascenseur, floor, terrasse, parking,
                   "Type", "City", "Nighberd", agency_city
            FROM data_casa
            UNION ALL
            SELECT new_price, chambres, "Sales_bain", surface,
                   ascenseur, floor, terrasse, parking,
                   "Type", "City", "Nighberd", agency_city
            FROM data_tanger
            UNION ALL
            SELECT new_price, chambres, "Sales_bain", surface,
                   ascenseur, floor, terrasse, parking,
                   "Type", "City", "Nighberd", agency_city
            FROM data_rabat;
        """))
        conn.commit()
        data_size_t =pd.read_sql("""select count(*) from unified_data """,engine)

        md_unified_data = f"""
        size of the data : {data_size_1}
        size of the updated data : {data_size_t}
        """
        create_markdown_artifact(key="unified-data-size",markdown=md_unified_data)
        return data_size_1,data_size_t