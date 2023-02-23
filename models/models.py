import sys
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6 import QtCore

class CustomQColumnModel(QStandardItemModel):
    """
    A class to hold the data to display in the QColumnView. A subclass of QStandardItemModel
    
    Attributes
    --------
        dba = a dictionary that holds all databases in the living database server, and their constituent tables

    Methods
    --------
        generate_tree():
            Convert the dictionary into QStandardItems that can be dynamically displayed by the QColumnView
    """
    #TODO: consider handling default behavior where no dictionary is passed in
    def __init__(self, dba=None):
        """
        Parameters:
        ----------
            dba : dictionary
                The dictionary of databases and tables
        """
        super(CustomQColumnModel, self).__init__()
        self.dba = dba 
        self.setVerticalHeaderItem(0, QStandardItem("Database"))
        self.setVerticalHeaderItem(1, QStandardItem("Table"))
 
    def generate_tree(self):
        """
        Convert the dictionary into QStandardItems that can be dynamically displayed by the QColumnView
        """
        # Here's the magic
        for row, db_name in enumerate(self.dba.keys()):
            self.setItem(row, 0, QStandardItem(db_name))
            item = self.item(row, 0)
            for rrow, table_name in enumerate(self.dba.get(item.text())):
                item.setChild(rrow, 0, QStandardItem(str(table_name)))


"""
    LivingDataListModel
    Overloaded constructor sets list data structure to what's given, or empty by default
    Note: This doesn't do anything anymore, but I'm keeping it in case I need it
"""
class LivingDataListModel(QtCore.QAbstractListModel):
    def __init__(self, db_list=None):
        super().__init__()
        self.db_list = db_list or []

    def data(self, index, role):
        # There are other roles outside of 'give me data to display'
        # so we'll specify our type of request when we call the method
        if role == Qt.DisplayRole:
            # Return only the text (forseeably the database name / table name)
            # given the column is always zero in a 1D list, so just return row
            return self.db_list[index.row()]

    def rowCount(self, index):
        return len(self.db_list)