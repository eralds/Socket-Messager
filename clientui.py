from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QMenu, QAction, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget, QLineEdit, QErrorMessage, QTextEdit, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import client

views = {"login": 0, "mainmenu": 1, "chat": 2, "group":3, "creategroup":4, "managegroup": 5}
app = QApplication(sys.argv)

online_button = QPushButton("Online")
ip_button = QPushButton("IPv4")
nickname_label = QLabel("")
users_list = QListWidget()
groups_list = QListWidget()
cur_groups_members = QListWidget()
messages_box = QTextEdit()
group_messages_box = QTextEdit()
group_chat_label = QLabel("Group")
group_chat_box = QLineEdit()
chat_label = QLabel("Chat")
chat_box = QLineEdit()
create_group_list = QListWidget()
group_name = QLineEdit()
manage_group_name = QLineEdit()
create_group_list.setSelectionMode(QAbstractItemView.MultiSelection)
manage_group_list = QListWidget()
manage_group_list.setSelectionMode(QAbstractItemView.MultiSelection)
manage_button = QPushButton("Modify group")





class ClientUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Client'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()
        
        
  
    
    def show_view(self, v):

        self.stacked_widget.setCurrentIndex(v)
        # if v == 1:
            # client.refreshMenu()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.stacked_widget = QStackedWidget()
        
        self.stacked_widget.addWidget(LoginView(self))
        self.stacked_widget.addWidget(MainMenuView(self))
        self.stacked_widget.addWidget(ChatView(self))
        self.stacked_widget.addWidget(GroupView(self))
        self.stacked_widget.addWidget(CreateGroupView(self))
        self.stacked_widget.addWidget(ManageGroupView(self))
        self.error_box = QErrorMessage()
        
        
  
        # Add a list widget to display connected clients
        # self.client_list_widget = QListWidget(self)
        # self.client_list_widget.setGeometry(10, 10, 580, 380)
        self.setCentralWidget(self.stacked_widget)

        # self.show()

    def showError(self, msg):
        self.error_box.showMessage(msg)
        
def LoginView(main_view):
    view = QWidget()
    label = QLabel("Nickname:")
    button = QPushButton("Connect")
    input_box = QLineEdit()
    ip_button.clicked.connect(lambda: client.toggleIp())
    button.clicked.connect(lambda: main_view.show_view(views["mainmenu"]) if client.connect(input_box.text()) else print())
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(ip_button)
    layout.addWidget(button)
    layout.addWidget(input_box)
    # layout.addWidget(error_box)
    view.setLayout(layout)
    return view

def ChatView(main_view):
    view = QWidget()
    button = QPushButton("Go back")
    button.clicked.connect(lambda: main_view.show_view(views["mainmenu"]))
    send = QPushButton("Send")
    send.clicked.connect(lambda: client.send_text(chat_box.text()))
    messages_box.setReadOnly(True)
    layout = QVBoxLayout()
    layout.addWidget(chat_label)
    layout.addWidget(button)
    layout.addWidget(messages_box)
    layout.addWidget(chat_box)
    layout.addWidget(send)
    view.setLayout(layout)
    return view

def GroupView(main_view):
    view = QWidget()
    button = QPushButton("Go back")
    button.clicked.connect(lambda: main_view.show_view(views["mainmenu"]))
    send = QPushButton("Send")
    send.clicked.connect(lambda: client.send_group_text(group_chat_box.text()))
    group_messages_box.setReadOnly(True)
    members_label = QLabel("Group members")
    manage_button.clicked.connect(lambda: main_view.show_view(views["managegroup"]))
    layout = QVBoxLayout()
    layout.addWidget(button)
    layout.addWidget(group_chat_label)
    layout.addWidget(group_messages_box)
    layout.addWidget(group_chat_box)
    layout.addWidget(send)
    layout.addWidget(members_label)
    layout.addWidget(cur_groups_members)
    layout.addWidget(manage_button)
    view.setLayout(layout)
    return view

def CreateGroupView(main_view):
    view = QWidget()
    label = QLabel("Create Group")
    name_label = QLabel("Name:")
    button = QPushButton("Go back")
    button.clicked.connect(lambda: main_view.show_view(views["mainmenu"]))
    create_button = QPushButton("Create")
    create_button.clicked.connect(lambda: client.createGroup(group_name.text(), create_group_list.selectedItems()))
    layout = QVBoxLayout()
    layout.addWidget(button)
    layout.addWidget(label)
    layout.addWidget(name_label)
    layout.addWidget(group_name)
    layout.addWidget(create_group_list)
    layout.addWidget(create_button)
    
    view.setLayout(layout)
    return view

def MainMenuView(main_view):
    view = QWidget()
    users_label = QLabel("Users")
    groups_label = QLabel("Groups")
    users_list.itemClicked.connect(lambda item: client.go_to_chat(item))
    groups_list.itemClicked.connect(lambda item: client.go_to_Groupchat(item))
    button2 = QPushButton("Go to groupchat")
    online_button.clicked.connect(lambda: client.toggleStatus())
    button2.clicked.connect(lambda: main_view.show_view(views["group"]))
    button3 = QPushButton("Create group")
    button3.clicked.connect(lambda: main_view.show_view(views["creategroup"]))
    layout = QVBoxLayout()
    layout.addWidget(nickname_label)
    layout.addWidget(online_button)
    layout.addWidget(users_label)
    # layout.addWidget(button)
    layout.addWidget(users_list)
    layout.addWidget(groups_label)
    # layout.addWidget(button2)
    layout.addWidget(groups_list)
    layout.addWidget(button3)
    view.setLayout(layout)
    return view

def ManageGroupView(main_view):
    view = QWidget()
    label = QLabel("Manage Group")
    change_users_label = QLabel("Modify users")
    name_label = QLabel("New name:")
    button = QPushButton("Go back")
    button.clicked.connect(lambda: main_view.show_view(views["group"]))
    manage_button = QPushButton("Save changes")
    manage_button.clicked.connect(lambda: client.manageGroup(manage_group_name.text(), manage_group_list.selectedItems()))
    layout = QVBoxLayout()
    layout.addWidget(button)
    layout.addWidget(label)
    layout.addWidget(name_label)
    layout.addWidget(manage_group_name)
    layout.addWidget(change_users_label)
    layout.addWidget(manage_group_list)
    layout.addWidget(manage_button)
    
    view.setLayout(layout)
    return view

    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ClientUI()
    ui.show() 
    sys.exit(app.exec_())
    
