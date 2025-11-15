from prefect.artifacts import create_markdown_artifact
from prefect.cache_policies import NO_CACHE
import pandas as pd 
from sqlalchemy import create_engine,text
import warnings
warnings.filterwarnings('ignore')



#### aggregation of the data ####
def aggregate_data(engine):
    table = pd.read_sql("""select "agency_city" ,count(*)  as "number_offers" , avg("new_price") as "avg_price" from unified_data 
                            group by "agency_city"
                            order by avg("new_price") desc
                        """,engine)
    table.to_sql('aggregation_table',engine,if_exists='replace',index=False)
    summary_md = table.to_markdown(index=False)
    create_markdown_artifact(
        key="aggegation-table-by-city",
        markdown=summary_md
    )
    return summary_md