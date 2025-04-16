import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
def fetch_data(output_dir='/opt/airflow/data/'):
    try:
        os.makedirs(output_dir,exist_ok=True)
        url = "https://www.worldometers.info/world-population/population-by-country/"
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find ALL tables
        tables = soup.find_all('table')
        # Loop through each table and save as CSV
        for i ,table in enumerate(tables,start=1):
            headers=[th.text.strip() for th in table.find_all('th')]
            # Extract data rows
            data=[]
            for row in table.find_all('tr')[1:]:
                cols=row.find_all('td')
                data.append([col.text.strip() for col in cols])
            df=pd.DataFrame(data,columns=headers)
            output_path=os.path.join(output_dir,f'table_{i}.csv')
            df.to_csv(output_path,index=False)
            print(f"Table {i} saved to: {output_path}")
        print(f"\nAll {len(tables)} tables saved to '{output_dir}'!")
        return output_path
    
    except Exception as e:
        raise Exception(f"ERROR: {e}")