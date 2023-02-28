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
            item.setEditable(False)
            print(type(item))
            for rrow, table_name in enumerate(self.dba.get(item.text())):
                item.setChild(rrow, 0, QStandardItem(str(table_name)))

class CustomQTableModel(QtCore.QAbstractTableModel):
    """
    A Custom model to popoulate a QTableView with a pandas dataframe

    Parameters
    ----------
        data: the dataframe that's passed in to initialize the table (model)
    """
    def __init__(self, data=None):
        #QtCore.QAbstractTableModel.__init__(self, parent)
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        # Returns length of a numpy representation of the pd dataframe
        # tells the data model how many row's we'll insert
        return len(self._data.values)

    def columnCount(self, parent=None):
        # tells the data model how many cols we'll insert
        return self._data.columns.size 

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            try:
                # .iat is just a good way to rol, col index dataframes in pd
                return str(self._data.iat[index.row(), index.column()])
            except IndexError:
                return ""

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
        if role == QtCore.Qt.DisplayRole:
            # given the column is always zero in a 1D list, so just return row
            return self.db_list[index.row()]

    def rowCount(self, index):
        return len(self.db_list)