import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()


def retrieve_rows():
    try:
        conn_string = f'postgresql+psycopg2://root:root@db:5433/test'
        engine = create_engine(conn_string)
        with engine.connect() as conn:
            # Create a SQLAlchemy text object for your query
            query = text("SELECT * FROM world_population LIMIT 10")
            result = conn.execute(query)
            for row in result:
                print(row)
    except Exception as e:
        raise Exception("Error retrieving rows:", e) from e