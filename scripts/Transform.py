import pandas as pd
from Extract import get_data
import os

def transform_data():
    # Read the CSV file
    path=get_data()
    df=pd.read_csv(path)

    # rename columns into correct format
    df.rename(columns={'#':'Index'},inplace=True)
    df.rename(columns={'UrbanPop %':'UrbanPop'},inplace=True)
    df.rename(columns={'Density(P/Km²)':'Density'},inplace=True)
    df.rename(columns={'Land Area(Km²)':'Land Area'},inplace=True)
    df.rename(columns={'Migrants(net)':'Migrants'},inplace=True)
    df.rename(columns={'Country (ordependency)':'Country'},inplace=True)
    df.rename(columns={'Population(2025)':'Population'},inplace=True)
    df.rename(columns={'Fert.Rate':'Fert_Rate'},inplace=True)
    df.rename(columns={'Land Area':'Land_Area'},inplace=True)


    # Edit values of each row
    df['YearlyChange']=df['YearlyChange'].apply(lambda x:x.replace('%','') if isinstance(x,str) and '%' in x else  x)
    df['YearlyChange']=df['YearlyChange'].apply(lambda x:x.replace('−','-') if isinstance(x,str) and '−' in x else  x)
    df['WorldShare']=df['WorldShare'].apply(lambda x:x.replace('%','') if isinstance(x,str) and '%' in x else  x)
    df['UrbanPop']=df['UrbanPop'].apply(lambda x:x.replace('%','') if isinstance(x,str) and '%' in x else  x)
    df['UrbanPop']=df['UrbanPop'].apply(lambda x:x.replace('%','') if isinstance(x,str) and '%' in x else  x)
    df['Land_Area']=df['Land_Area'].apply(lambda x:x.replace(',','') if isinstance(x,str) and ',' in x else  x)
    df['Land_Area']=df['Land_Area'].apply(lambda x:x.replace('−','-') if isinstance(x,str) and '−' in x else  x)
    df['NetChange']=df['NetChange'].apply(lambda x:x.replace(',','') if isinstance(x,str) and ',' in x else  x)
    df['NetChange']=df['NetChange'].apply(lambda x:x.replace('−','-') if isinstance(x,str) and '−' in x else  x)
    df['Population']=df['Population'].apply(lambda x:x.replace(',','') if isinstance(x,str) and ',' in x else  x)
    df['Population']=df['Population'].apply(lambda x:x.replace('−','-') if isinstance(x,str) and '−' in x else  x)
    df['Migrants']=df['Migrants'].apply(lambda x:x.replace('−','-') if isinstance(x,str) and '−' in x else  x)
    df['Migrants']=df['Migrants'].apply(lambda x:x.replace(',','') if isinstance(x,str) and ',' in x else  x)
    df['Density']=df['Density'].apply(lambda x:x.replace(',','') if isinstance(x,str) and ',' in x else  x)

    # Edit the Dtypes of columns
    df['WorldShare']=df['WorldShare'].astype(float)
    df['UrbanPop']=df['UrbanPop'].astype(float)
    df['MedianAge']=df['MedianAge'].astype(float)
    df['Migrants']=df['Migrants'].astype(int)
    df['Land_Area']=df['Land_Area'].astype(int)
    df['Density']=df['Density'].astype(int)
    df['NetChange']=df['NetChange'].astype(int)
    df['YearlyChange']=df['YearlyChange'].astype(float)
    df['Population']=df['Population'].astype(int)
    df['Country']=df['Country'].astype(str)


    # save the data
    os.makedirs('/opt/airflow/data/', exist_ok=True)

# Save the DataFrame
    df.to_csv('/opt/airflow/data/Transformed_data.csv', index=False)
transform_data()