# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 21:21:50 2025

@author: brian
"""
import psycopg2
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv('.env')

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
    


# Print out the columns associated with a table
for key, value in tables_columns.items():
    print('-'*50)
    print('Table: ', key)
    print('Columns: ', value)
    print('Column Types:')
    for v in value:
        print(v, ',',  f'{column_types[v]}')
    print('\n')
    print('-'*20)
print('Columns Types: ', column_types)




# Connect and push the data into the PostgreSQL on OnRender
#pg_conn = psycopg2.connect(host=os.getenv("host"), dbname=os.getenv("dbname"), user=os.getenv("user"),
#                        password=os.getenv("password"), port=os.getenv("port"))
#pg_cur = pg_conn.cursor()



#pg_cur.execute(
f"""
CREATE TABLE IF NOT EXISTS {table[0]} (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR);
"""
#    )

#pg_cur.execute(
"""
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
"""
#    )

#print(pg_cur.fetchall())

#pg_conn.commit()

#pg_cur.close()
#pg_conn.close()