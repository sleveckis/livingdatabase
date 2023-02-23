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
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from Ui_MainWindow import Ui_MainWindow
from models.DatabaseConnect import DatabaseConnector
from models.models import CustomQColumnModel

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
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
        # Instantiate column model object as MainWindow attribute (good practice?)
        self.db_connection = DatabaseConnector()
        self.model = CustomQColumnModel(self.db_connection.databases)
        self.model.generate_tree() 

        # Access the col view widget in our app here, via inheritance, and set it to MainWindow's model
        # self.livdbListView.setModel(LivingDataListModel(list_o_dbs))
        self.ColumnView.setModel(self.model)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
# Pass exit code to system
sys.exit(app.exec())