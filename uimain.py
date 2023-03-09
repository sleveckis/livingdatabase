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
from PySide6.QtCore import QItemSelectionModel, QFile, QTextStream
from Ui_MainWindow import Ui_MainWindow
from models.DatabaseConnect import DatabaseConnector
from models.models import CustomQColumnModel, CustomQTableModel

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The primary container for all of the GUI. A subclass of both QMainWindow from PySide, and Ui_Mainwindow, the generated
    module derivitave of Qt Designer.

    Contains all behavior that responds to user interaction

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
        self.ColumnView.setAutoScrollMargin(1)
        
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
    def colViewClick(self):
        """
            Get the table/database the user clicked on, and the containing database if it was a table they clicked on.
            Get the relevant table by calling a funciton to connect to the database, set the table view's model to
            the returned table, and display it.
            Only execute the table query if the user actually clicked on a table, not a database.
        """
        # Get the index to pass to the column model based on user click
        user_select_index = self.ColumnView.selectedIndexes()[0]
        # Get the QStandardItem object from the column model based on index
        item = self.col_model.itemFromIndex(user_select_index)

        item_text = item.text()
        parent_item = item.parent()

        # If the item is a table
        if parent_item is not None:
            db_name = parent_item.text()
            # Get table as a pandas dataframe, passing in database name and table name
            table = self.db_connection.get_table_contents(database=db_name, table=item_text, n=self.tableSize)
            # Make a table model with the dataframe, and set the Table View to it
            self.table_model = CustomQTableModel(table)
            self.TableView.setModel(self.table_model)

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.setWindowTitle("Living Database")
window.setWindowIcon(QtGui.QIcon('media/netl_logo_small_transparent.png'))
# Apply non-standard theme
StyleFile = QFile("styles/custom/Custom.qss")
if StyleFile.open(QFile.ReadOnly | QFile.Text):
    qss = QTextStream(StyleFile)
    app.setStyleSheet(qss.readAll())
window.show()
# Pass exit code to system
sys.exit(app.exec())