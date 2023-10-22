from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys



                
class ServerUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Server'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Add a list widget to display connected clients
        self.client_list_widget = QListWidget(self)
        self.client_list_widget.setGeometry(10, 10, 580, 380)

        self.show()

    def add_client(self, name):
        # Add a new item to the list widget for the new client
        item = QListWidgetItem()
        item.setText(f"{name} - Online")
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.client_list_widget.addItem(item)

    def remove_client(self, name):
        # Remove the item from the list widget for the disconnected client
        for i in range(self.client_list_widget.count()):
            item = self.client_list_widget.item(i)
            if name in item.text():
                self.client_list_widget.takeItem(i)
                break

    def set_client_status(self, name, online):
        # Set the online/offline status for the client in the list widget
        for i in range(self.client_list_widget.count()):
            item = self.client_list_widget.item(i)
            if name in item.text():
                if online:
                    item.setText(f"{name} - Online")
                else:
                    item.setText(f"{name} - Offline")
                break


def display():
    app = QApplication(sys.argv)
    ui = ServerUI()
    # ui.show() 
    # sys.exit(app.exec_())
    return ui
    
if __name__ == "__main__":
    display()
