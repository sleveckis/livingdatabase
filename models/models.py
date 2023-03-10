import sys
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6 import QtCore

class CustomQColumnModel(QStandardItemModel):
    """
    A class to hold the data to display in the QColumnView. A subclass of QStandardItemModel, which is subclassed from QAbstractitemModel
    
    Attributes
    --------
        dba = a dictionary that holds all databases in the living database server, and their constituent tables
        databaseListLength = how long the first list in the cascade view is (# of databases)
        tableListLengths = a list of how many tables belong to each database, indexed in order of database 

    Methods
    --------
        generate_tree():
            Convert the dictionary into QStandardItems that can be dynamically displayed by the QColumnView, 
            by setting the inherited setItem() function for QStandardItemModel
    """
    def __init__(self, dba=None):
        """
        Parameters:
        ----------
            dba : dictionary
                The dictionary of databases and tables
        """
        super(CustomQColumnModel, self).__init__()
        if dba is not None:
            self.dba = dba 
            self.sort_dba_alphabetically()
            self.setVerticalHeaderItem(0, QStandardItem("Database"))
            self.setVerticalHeaderItem(1, QStandardItem("Table"))
            self.databaseListLength = 0
            self.tableListLengths = []
        else:
             dba = {}
 
    def generate_tree(self):
        """
        Set each database name as an item, and set each table therein as a child of the corresonding item
        setItem(row, col, item)
            sets an item at the given row and column
        item(row, col)
            returns the tiem for the given row and column

        NOTE: There's a bug that prints an invalid index error to the console when clicking on a *database*
        after having clicked on a *table*, if that database's row count is greater than 2 (zero-indexed).
        It appears to have no effect on program behavior. 
        """
        for row, db_name in enumerate(self.dba.keys()):
            self.setItem(row, QStandardItem(str(db_name)))
            item = self.item(row)
            item.setEditable(False)

            table_count = 0
            for rrow, table_name in enumerate(self.dba.get(item.text())):
                item.setChild(rrow, QStandardItem(str(table_name)))
                table_count +=1

            self.tableListLengths.append(table_count)
        self.databaseListLength = len(self.tableListLengths)

    def sort_dba_alphabetically(self):
        self.dba = dict(sorted(self.dba.items()))
        for table_list in self.dba:
            self.dba[table_list] = sorted(self.dba[table_list])

        
            

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
        self._dataframe = data

        if data is None:
            # Display 'no table' message
            pass

    def rowCount(self, parent=None):
        # Returns length of a numpy representation of the pd dataframe
        # tells the data model how many row's we'll insert
        if self._dataframe is None:
            return 0
        else:
            return len(self._dataframe.values)

    def columnCount(self, parent=None):
        # tells the data model how many cols we'll insert

        if self._dataframe is None:
            return 0
        else:
            return self._dataframe.columns.size 

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if self._dataframe is not None:
            if role == QtCore.Qt.DisplayRole:
                try:
                    # .iat is just a good way to rol, col index dataframes in pd
                    return str(self._dataframe.iat[index.row(), index.column()])
                except IndexError:
                    return ""


    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        Basically, allow the user to see the column headers 
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == QtCore.Qt.Vertical:
                # Add one so the row counts start at 1, not zero
                return str(self._dataframe.index[section] + 1)

        return None           

class CustomThread(QtCore.QThread):

    newProgress = QtCore.Signal(str)

    def __init__(self, i):
        super(MyProcess, self).__init__()
        self.id = i

    def run(self):
        for j in range(10):
            self.newProgress.emit('task %d at %d%%' % (self.id, j*10))
            time.sleep(0.2)


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