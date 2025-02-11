# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:18:46 2025

@author: brian
"""

import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

# Loading the environment variables
load_dotenv('.env',override=True)

# =============================================================================
# Read the csv file from the local storage from https://www.cdc.gov/bird-flu/situation-summary/index.html
csv_file = r'C:\Users\brian\Downloads\commercial-backyard-flocks.csv'
df = pd.read_csv(csv_file)

print('Columns:\n', df.columns)
print('\n')
print('Column types: \n', df.dtypes)
print('Infomation: \n', df.info)
print('\n')
# =============================================================================
# Turning the Outbreak date type from object to datetime. 
df['Outbreak Date'] = pd.to_datetime(df['Outbreak Date'])

print('Column types: \n', df.dtypes)
print('\n')


# =============================================================================




# =============================================================================
# Connect and push the data into the PostgreSQL on OnRender

# pg_conn = psycopg2.connect(host=os.getenv("host"), dbname=os.getenv("dbname"), user=os.getenv("user"),
#                             password=os.getenv("password"), port=os.getenv("port"))
# pg_cur = pg_conn.cursor()
postgreSQL_url = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}.ohio-postgres.render.com/{os.getenv("dbname")}'
pg_conn = create_engine(postgreSQL_url)

# =============================================================================
# Convert the dataframe to sql.

try:
    df.to_sql(name='avian_flu', con=pg_conn, chunksize=5000, index=True, index_label='id', if_exists='replace')   
    print('*'*30)
    print('Successfully Migrated!')
    print('*'*30)
except ValueError:
    print('*'*30)
    print('It was not successful')
    print('*'*30)
    
    
# =============================================================================
# Execute a query to verify whether it was successful on PostgreSQL server side. 
pg_conn = psycopg2.connect(host=os.getenv("host"), dbname=os.getenv("dbname"), user=os.getenv("user"),
                            password=os.getenv("password"), port=os.getenv("port"))
pg_cur = pg_conn.cursor()

pg_cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'avian_flu'")

for result in pg_cur.fetchall():
    print('result:\n', result)
print('\n')
pg_cur.execute(
    """
    alter table avian_flu 
    add primary key (id);
    """
    )

pg_conn.commit()

#print(pg_cur.fetchall())

pg_cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'avian_flu'")

for result in pg_cur.fetchall():
    print('result:\n', result)
print('\n')
               
pg_cur.execute(
    """
    SELECT * FROM avian_flu
    LIMIT 10;
    """
    )

for result in pg_cur.fetchall():
    print('result:\n', result)
print('\n')


# =============================================================================
# Close the connection

# pg_cur.close()
# pg_conn.close()