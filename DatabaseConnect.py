import psycopg2
import pandas as pd

"""
    Connects to hard-coded server in conn_string
    :retuns: database_list: single list of all databases in the database server we connect to
"""
def connect_and_return_databases():
    # create connection string
    conn_string = 'postgresql://postgres:l1v1ngD4t4b4s3!@10.67.10.38:5005'
    #connect to database with connection string
    pg_conn = psycopg2.connect(conn_string)
    cur = pg_conn.cursor()
    cur.execute("""SELECT datname FROM pg_catalog.pg_database""")
    databases = cur.fetchall()
    database_list = []
    for d in databases:
        database_list.append(d[0])

    return (database_list)

