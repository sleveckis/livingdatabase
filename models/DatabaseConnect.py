import psycopg2
import pandas as pd

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
        self.cursor = self.cursor_to_server()
        self.databases = self.get_databases(self.cursor)

    def cursor_to_server(self):
        """
        Returns:
        ---------
            cur
                A connection to the living database
        """
        conn_string = 'postgresql://postgres:l1v1ngD4t4b4s3!@10.67.10.38:5005'
        pg_conn = psycopg2.connect(conn_string)
        cur = pg_conn.cursor()
        return cur

    def get_databases(self, cur):
        """
        Parameters:
        ---------
            cur
                A connection to the living database

        Returns:
        ---------
            database_dict
                A dictionary of all the databases within the living database
        """
        # Replace with query from Mike to get a dictionary as in the docstring
        cur.execute("""SELECT datname FROM pg_catalog.pg_database""")
        databases = cur.fetchall()
        database_list = []
        for d in databases:
            database_list.append(d[0])

        test_dba = {
            "dab1":  [101, "hellow", "yeehaw"],
            "dab2":  [202, "salutations", "cowabunga"],
            "dab3":  [303, "greetings", "weeeee"],
            "dab4":  [404, "howdy", "expelliarmus"],
        }
        return test_dba
        #return (database_list)

    def get_table_contents(self, table, n):
        pass


