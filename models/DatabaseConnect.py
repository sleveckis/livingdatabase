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
        self.databases = self.get_databases()

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

    def get_databases(self):
        """
        Returns:
        ---------
            database_dict
                A dictionary of all the databases within the living database
        """
        # Replace with query from Mike to get a dictionary as in the docstring

        self.cursor.execute("""SELECT datname FROM pg_catalog.pg_database""")
        databases = self.cursor.fetchall()
        database_list = []
        for d in databases:
            database_list.append(d[0])

        test_dba = {
            "CoolDatabase":  ["tableForTwo", "cooltableNice", "mySweetTable", "usefulTable", "niceTableToHave"],
            "EvilDatabase":  ["villainousTable"],
            "RegularDatabase":  ["tableOfHotDogs", "roundTable", "partyTable"],
            "ScienceDatabase":  ["tableOfFrogs", "taleOfNewts", "coolRocks.bizTable"],
            "UselessDatabase":  ["oldTable", "emptyTable", "corruptTable"],
            "ThisIsADatabase":  ["thatTable", "thisTable", "standardTable", "extraTable"]
        }
        return test_dba
        #return (database_list)

    #TODO: Because we're getting database names and table names, do a try block or something. Or use a filter. 
    # Don't want to query a tablename where tablename is actually a databasename
    def get_table_contents(self, table=None, n=None):
        test_table = {
            "What Rock" : ["Basalt", "shale", "obsidian", "quartz", "sdfsfs", "asdfasdf", "sdfasdf", "asdf", "marble"],
            "How old is rock" : [101, 202, 333, 40151, 1551515, 663, 991, 123, 12],
            "calories" : [123, 4141, 52343, 123123, 235234, 5345, 2312, 534534, 12313],
            "phone number" : [23123, 12312, 53453, 867, 56567, 9878990 , 56986, 234243, 90897]
        }

        # Placeholder code... switch out with a real query with table name
        test_table["What Rock"][0] = table
        df = pd.DataFrame(test_table)

        # SQL Query where we get the first n rows of table 'table'
        # return that dataframe instead
        return df


