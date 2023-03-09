"""
    uimain.py
    02-20-2023
    Author: Leveckis

    Borrowing QAbstractListModel subclassing via 
    https://www.pythonguis.com/tutorials/pyside6-modelview-architecture/

    Borrowing QStandardItemModel subclassing (which is what I actually use for QColumnView) via
    https://bancaldo.wordpress.com/2019/05/16/pyqt5-qcolumnview/
"""

import sys
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PySide6.QtCore import QItemSelectionModel
from Ui_MainWindow import Ui_MainWindow
from models.DatabaseConnect import DatabaseConnector
from models.models import CustomQColumnModel, CustomQTableModel

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The primary container for all of the GUI. A subclass of both QMainWindow from PySide, and Ui_Mainwindow, the generated
    module derivitave of Qt Designer.

    Attributes:
    ----------
        ui : Ui_MainWindow
            Instance of the Ui_MainWindow class
        db_connection : DataBaseConnector
            Instance of the DatabaseConnector class
        model: CustomQColumnModel
            Instance of CustomQColumnModel, initialized with the dictionary of databases/tables  

    Important Inherited Attributes
    ---------
        ColumnView : QColumnView (from Ui_MainWindow)
            QColumnView is a subclass of QAbstractItemView

        TableView : QTableView (from Ui_MainWindow)
            QColumnView is a subclass of QAbstractItemView

    """
    def __init__(self):
        # Ui_MainWindow has no __init__() so it defaults to QMainWindow's constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # Database object
        self.db_connection = DatabaseConnector()

        # Column Model/View
        self.col_model = CustomQColumnModel(self.db_connection.master_dict)
        self.col_model.generate_tree() 
        self.ColumnView.setModel(self.col_model)
        # only disables innermost list. similar code in models.py for outer list
        self.ColumnView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Table Model/View
        # Potentially don't need to start with empty table/model. Keep for now.
        self.table_model = CustomQTableModel()
        self.TableView.setModel(self.table_model)
        self.TableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Display first x rows of table 
        self.tableSize = 100

        # Connect user interaction to relevant methods
        self.create_connections()

    def create_connections(self):
        self.ColumnView.clicked.connect(self.colViewClick)

    # Slots
    """
        Get a table as a dataframe and set it as the TableView's model so the user can see it
    """
    def colViewClick(self):
        # Get the text of whatever table the user has selected
        user_select_index = self.ColumnView.selectedIndexes()[0]
        # The relevant QStandardItem object in the Column Model
        item = self.col_model.itemFromIndex(user_select_index)
        item_text = item.text()
        parent_item = item.parent()
        
        # If the item is a database
        if parent_item is None:
            print("---------------------------------")
            print("DATABASE: ", item_text)
            print("---------------------------------")
            item_is_table = False

        # If the item is a table
        else:
            db_name = parent_item.text()
            item_is_table = True
            print("---------------------------------")
            print("Table: ", item_text)
            print("Table's parent databae: ", db_name)
            print("---------------------------------")


            # Get table as a pandas dataframe, passing in database name and table name
            table = self.db_connection.get_table_contents(database=db_name, table=item_text, n=self.tableSize)
            # Make a table model with the dataframe, and set the View to it
            self.table_model = CustomQTableModel(table)
            self.TableView.setModel(self.table_model)
    """

    # Old method of implementation

    def colViewClick(self):
        # Get the text of whatever table the user has selected
        user_select_index = self.ColumnView.selectedIndexes()[0]
        # item = user_select_index.data()
        item = self.col_model.itemFromIndex(user_select_index)
        item_text = item.text()
        print("Item string/text: ", item_text)

        parent_item = item.parent()
        if parent_item is not None:
            print("---------------------------------")
            print("Hopefully the relevant database: ", parent_item.text())
            print("---------------------------------")
        else:
            print("~~~~This is a database, it has no parent")

        # Check to see if the user selected item is a database or table
        dict_keys = list(self.db_connection.master_dict.keys())
        dict_vals = list(self.db_connection.master_dict.values())
        clickIsTable = False
        try:
            dict_keys.index(item_text)
        except:
            # It's a table
            clickisTable = True
        else:
            # It's a database
            print("That's not a table that's a database!")

        if clickIsTable is False:            
            dict_index = None
            print("Dict index (should be None):", dict_index)
            for count, table in enumerate(dict_vals):
                try:
                    table.index(item_text)
                except:
                    pass
                else:
                    dict_index = count

            
            if dict_index is not None:
                db_name = dict_keys[dict_index]
                print("Dict index:", dict_index)
                print("Database: ", db_name)
                print("Table: ", item_text)
                print("--------------------------------")

                # Get table as a pandas dataframe, passing in database name and table name
                table = self.db_connection.get_table_contents(database=db_name, table=item_text, n=self.tableSize)
                # Make a table model with the dataframe, and set the View to it
                self.table_model = CustomQTableModel(table)
                self.TableView.setModel(self.table_model)
    """

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.setWindowTitle("Living Database")
window.setWindowIcon(QtGui.QIcon('media/small_logo.png'))
window.show()
# Pass exit code to system
sys.exit(app.exec())