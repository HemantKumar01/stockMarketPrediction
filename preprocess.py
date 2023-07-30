import json
import os
from datetime import datetime
import pandas as pd


data_path = "./data_collection/news_data/"
output_path = "./preprocessed/"


raw_preprocessed_data = []
preprocessed_data = None


def news_count():
    global raw_preprocessed_data,preprocessed_data

    news_files = os.listdir(data_path)
    for file_name in news_files:
        if file_name == "fallback.json":
            continue

        date = datetime.strptime(file_name[10:20], "%d-%m-%Y")
        news_data = json.dump(data_path + file_name)
        raw_preprocessed_data.append({"date": date, "n_news": len(news_data)})
    
    preprocessed_data = 

def preprocess():
    news_count()


if 
    preprocess();