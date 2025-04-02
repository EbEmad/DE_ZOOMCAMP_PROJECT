import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_data(output_dir='data',output_filename="world_population.csv"):
    try:
        os.makedirs(output_dir,exist_ok=True)
        output_path=os.path.join(output_dir,output_filename)
        if os.path.exists(output_path):
            print(f"{output_path} already exists , skipping downloading")
            return None
        url = "https://www.worldometers.info/world-population/population-by-country/"
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the table (assuming it's the first table on the page)
        table = soup.find('table')
        # Extract table rows
        rows = table.find_all('tr')
        # Extract headers (column names)
        headers = [th.text.strip() for th in rows[0].find_all('th')]
        # Extract data rows
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            data.append([col.text.strip() for col in cols])
        
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(output_path, index=False)
        
        print(f"Data successfully saved to {output_filename}!")
        return df
    
    except Exception as e:
        raise Exception(f"ERROR: {e}")

# Usage
if __name__=='__main__':
    get_data()