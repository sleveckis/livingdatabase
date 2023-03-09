import psycopg2
import pandas as pd
from urllib.parse import urlparse

class DatabaseConnector():
    """
    A class to connect to the living database and get/store relevant information

    Attributes:
    ----------
        cursor: the "cursor" (ie, connection) to the living database server
        databases: a dictionary with databases as indices and their constituent tables as keys
    
    Methods:
    ----------
        cursor_to_server()
            Connects to, and returns a cursor from, the server which is passed to other methods to execute SQL queries

        get_databases(cur)
            Returns a dictionary of databases and their tables

        TODO:
        get_table_contents(table, n):
            Returns the first n rows of a table as a [pandas dataframe?]
        
    """
    def __init__(self):
        self.conn_string ='postgresql://postgres:l1v1ngD4t4b4s3!@10.67.10.38:5005'
        self.cursor = self.cursor_to_server()
        self.master_dict = self.get_databases_and_tables()

    def cursor_to_server(self):
        """
        Returns:
        ---------
            cur
                A connection to the living database
        """
        conn_string_old = 'postgresql://postgres:l1v1ngD4t4b4s3!@10.67.10.38:5005'
        # Parsing old string into a dictionary so I can change dbname easily
        p = urlparse(conn_string_old)
        pg_connection_dict = {
            'dbname': p.path[1:],
            'user': p.username,
            'password': p.password,
            'port': p.port,
            'host': p.hostname
        }
        pg_conn = psycopg2.connect(**pg_connection_dict)
        cur = pg_conn.cursor()
        return cur

    def get_databases_and_tables(self):
        """
        Returns:
        ---------
            database_dict
                A dictionary of all the databases within the living database
        """
        # First, get all databases into a list, database_list
        fetch_query = ("""SELECT datname FROM pg_catalog.pg_database""")
        self.cursor.execute(fetch_query)
        databases = self.cursor.fetchall()
        database_list = []
        for d in databases:
            database_list.append(d[0])
        num_databases = len(database_list)

        for d in database_list:
            print(d)
        print("Number of databases: ", num_databases)

        # Then, connect to each database and store its tables 
        p = urlparse(self.conn_string)
        temp_connection_dict = {
            'dbname': d,
            'user': p.username,
            'password': p.password,
            'port': p.port,
            'host': p.hostname
        }

        master_dictionary = {}

        print("Gathering database info... this may take a second...")
        # Connect to each database and save all its table names to a list
        for d in database_list:
            temp_connection_dict['dbname'] = d
            try:
                temp_conn = psycopg2.connect(**temp_connection_dict)
            except:
                print("\tRats! Failed on: ", temp_connection_dict['dbname'])
                # If you don't remove failed databases, master dictionary keys/values will be mismatched later
                database_list.remove(d)
            else:

                cur = temp_conn.cursor()
                # This query gets a list of all table names from the current database (d in database_list)
                cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'postgres' and table_type = 'BASE TABLE' or table_schema = 'public' and table_type = 'BASE TABLE';""")
                temp_list = []
                for t in cur.fetchall():
                    temp_list.append(t[0])

                # Create a dictionary entry of the corresponding database and list of tables
                master_dictionary[d] = temp_list

                # Uncomment these to get terminal printout of database name and its tables
                """
                print("Success on: ", temp_connection_dict['dbname'])
                print(temp_list)
                print("----------------------")
                """
        return master_dictionary

    #TODO: Because we're getting database names and table names, do a try block or something. Or use a filter. 
    # Don't want to query a tablename where tablename is actually a databasename

    def get_table_contents(self, database=None, table=None, n=None):
        # Placeholder code... switch out with a real query with table name
        conn_string = self.conn_string + '/' + database

        # If a table name contains an uppercase letter, we need to put it in quotation marks
        # because of some horrible old ANSI standard for goblins
        if self.contains_upper(table):
            table = f'"{table}"'

        print("-------------------------------------------")
        print("Connecting to ", database, "with table", table)
        print("conn_string: ", conn_string)
        print("-------------------------------------------")

        with psycopg2.connect(conn_string) as pg_conn:
            sql = "select * from {0} LIMIT 100".format(table)
            df = pd.read_sql_query(sql, pg_conn)
            print(df)

        return df

    def contains_upper(self, input):
        result = False
        for character in input:
            if character.isupper():
                result = True
        return result

