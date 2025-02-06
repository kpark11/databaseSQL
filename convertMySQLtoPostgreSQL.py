# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 21:21:50 2025

@author: brian
"""
# import psycopg2
import sqlite3
from dotenv import load_dotenv
import os
import re
import pandas as pd
from sqlalchemy import create_engine

load_dotenv('.env')

# =============================================================================
# Connect and get the data from the local database, which is in the format of MySQL
local_db = r'C:\Users\brian\OneDrive - University of Tennessee\Desktop\Research\Python program\Springboard\SQLFiles-Tier-2-Unit-8\sqlite_db_pythonsqlite.db'
sqlite_con = sqlite3.connect(local_db)
sqlite_cur = sqlite_con.cursor()
# getting tables
sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = sqlite_cur.fetchall()
# getting tables
print('*'*50)
print('TABLES:', tables)
print('\n\n')
print('*'*50)
tables_columns = {}
column_types = {}
for table in tables:
    # This line will return CREATE TABLES with various variables and its type
    # sqlite_cur.execute(f"SELECT sql FROM sqlite_master WHERE name='{table[0]}'")
    
    # we can try other way to learn more about it
    sqlite_cur.execute(f"SELECT * FROM '{table[0]}'")
    sqlite_cur.fetchone()
    columns = []
    
    for column in sqlite_cur.description:
        columns.append(column[0])
    tables_columns[f'{table[0]}'] = columns
    
    descriptions = {}
    sqlite_cur.execute(f'PRAGMA table_info({table[0]});')
    describe = sqlite_cur.fetchall()
    for description in describe:
        column_types[description[1]] = description[2]
    
    
# Getting ready for the conversion into Postgresql from sqlite
# The decimal is numeric
# The int(n,m) is now just int
for col,types in column_types.items():
    if re.match('int',types):
        column_types[col] = 'INT'
    elif re.match('decimal',types):
        types = types.split('(')[-1].split(')')[0]
        column_types[col] = f'NUMERIC({types})'
    else:
        pass

print(column_types)



# Print out the columns associated with a table
for key, value in tables_columns.items():
    print('-'*50)
    print('Table: ', key)
    print('\n')
    print(f'Columns ({len(value)}): ', value)
    print('\n')
    print('Column Types:')
    for i,v in enumerate(value):
        print(i+1, v, ',',  f'{column_types[v]}')
    print('\n')
    print('-'*20)
print(f'Columns Types: {len(column_types)}', column_types)
# =============================================================================




# =============================================================================
# Connect and push the data into the PostgreSQL on OnRender

# pg_conn = psycopg2.connect(host=os.getenv("host"), dbname=os.getenv("dbname"), user=os.getenv("user"),
#                             password=os.getenv("password"), port=os.getenv("port"))
# pg_cur = pg_conn.cursor()
postgreSQL_url = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}.ohio-postgres.render.com/{os.getenv("dbname")}'
pg_conn = create_engine(postgreSQL_url)


# Using pandas 

for table in tables:    
    table_split = [t for t in re.split("([A-Z][^A-Z]*)", table[0]) if t]
    table_split = '_'.join(table_split)
    table_split = table_split.lower()
    df = pd.read_sql(f'SELECT * FROM {table[0]}', con=sqlite_con)
    print(df.head())
    df.to_sql(name=table_split, con=pg_conn, chunksize=5000, index=False, index_label=False, if_exists='replace')    
    
# =============================================================================
# pg_cur.execute(
#     """
#     SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
#     """
#     )

# print(pg_cur.fetchall())
# =============================================================================
# Closing them
sqlite_cur.close()
sqlite_con.close()

# pg_conn.commit()

# pg_cur.close()
# pg_conn.close()
# =============================================================================
