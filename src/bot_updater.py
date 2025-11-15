from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from prefect import task,flow


### for sucess reporting
def send_repport_success(data_size_1,data_size_t):

    load_dotenv(dotenv_path='../.env')
    key = os.getenv("bot_key")
    chat_id = os.getenv("chat_id")
    message = f"""
    date : {datetime.today()}
    the data pipeline completed successfully :\n
    **the pipeline status:**\n
    -----------------------------------
    |data size in t-1 :| {data_size_1}|
    -----------------------------------
    |data size in t : {data_size_t}|\n
    -----------------------------------
    """
    
    url = f"https://api.telegram.org/bot{key}/sendMessage"
    payload = {"chat_id":chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url,data=payload)



 ### for error repporting   

def send_repport_error(error):

    load_dotenv(dotenv_path='../.env')
    key = os.getenv("bot_key")
    chat_id = os.getenv("chat_id")
    error = str(error)
    error = error.replace('_','')
    message = f"""
    ---------------------------------------------------------
    date : {datetime.today()} \n
    housing data pipeline
    ---------------------------------------------------------
    the pipeline status:\n
    Status: ❌ FAILED**  
    Error: {str(error)} """

    url = f"https://api.telegram.org/bot{key}/sendMessage"
    payload = {"chat_id":chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url,data=payload)



