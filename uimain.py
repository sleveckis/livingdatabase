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
    """
    def __init__(self):
        # Ui_MainWindow has no __init__() so I guess it defaults to QMainWindow's constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # Column Model
        self.db_connection = DatabaseConnector()
        self.col_model = CustomQColumnModel(self.db_connection.databases)
        self.col_model.generate_tree() 
        self.ColumnView.setModel(self.col_model)
        # only disables innermost list. similar code in models.py for outer list
        self.ColumnView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Table Model
        self.table_model = CustomQTableModel(self.db_connection.get_table_contents())
        self.TableView.setModel(self.table_model)
        self.TableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.setWindowTitle("Living Database")
window.setWindowIcon(QtGui.QIcon('media/small_logo.png'))
window.show()
# Pass exit code to system
sys.exit(app.exec())