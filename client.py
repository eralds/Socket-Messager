import socket
import clientui
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime, Qt
import sys

chat_history = {}
group_history = {}
class Handler(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(object)
    def __init__(self, client):
        super().__init__()
        self.client= client
    def run(self):
        while True:
            try:
                msg = self.client.recv(1024).decode("utf8")
                self.messageReceived.emit(msg)
            except Exception as e:
                print(str(e))
                
class Client():
    def __init__(self):
        
        # self.app = QApplication(sys.argv)
        self.ui = clientui.ClientUI()
        clientui.client=self
        self.nickname=""
        self.online = True
        self.reciever= ""
        self.group = ""
        self.ip = socket.AF_INET
        # show_thread = threading.Thread(target=self.ui.show)
        # show_thread.start()

        self.ui.show() 
        sys.exit(clientui.app.exec_())
        
    def toggleStatus(self):
        if self.online:
            self.online = False
            clientui.online_button.setText("Offline")
            self.client.send(("STATUS:OFFLINE\n").encode('utf-8'))
        else: 
            self.online = True   
            clientui.online_button.setText("Online") 
            self.client.send(("STATUS:ONLINE\n").encode('utf-8'))
    def toggleIp(self):
        if self.ip == socket.AF_INET:
            self.ip = socket.AF_INET6
            clientui.ip_button.setText("IPv6")
        else:   
            self.ip = socket.AF_INET
            clientui.ip_button.setText("IPv4")
            
            
    def createGroup(self, name, selectedItems):
        self.client.send(( "CREATEGROUP:" + name+":"+ ",".join([item.text() for item in selectedItems])).encode("utf-8"))
        clientui.group_name.clear()
        self.ui.show_view(clientui.views["mainmenu"])
    
    def manageGroup(self, name, selectedItems):
        self.client.send(( "MANAGEGROUP:" +self.group +":"+ name+":"+ ",".join([item.text() for item in selectedItems])).encode("utf-8"))
        clientui.manage_group_name.clear()
        self.ui.show_view(clientui.views["mainmenu"])   
        
    def connect(self,nick):
        if nick == "" or ":" in nick:
            self.ui.showError("Nickname shouldn't be empty or contain a ':'")
            return False
        try:
            self.nickname = nick
            clientui.nickname_label.setText(nick)
            self.ui.setWindowTitle(nick)
            
                # Connecting To Server
            self.client = socket.socket(self.ip, socket.SOCK_STREAM)
            self.client.connect(('localhost', 8081))

            # message = 'NICK:{}'.format(nickname)

            # receive_thread = threading.Thread(target=self.receive)
            # receive_thread.start()

            # write_thread = threading.Thread(target=self.write)
            # write_thread.start()
                # Starting Threads For Listening And Writing
            self.handler = Handler(self.client)
            self.handler.messageReceived.connect(self.handle)
            self.handler.start()
            # client.send(message.encode('utf-8'))
            return True
        except:
            self.ui.showError("Can't connect")
            return False #change later
           
   
             
    # Listening to Server and Sending Nickname
    def handle(self, message):
        # while True:
        try:
            #see if user is on the groupchat window             
            for message in message.split("\n"):
                if message == 'NICK':
                    self.client.send(("NICK:" + self.nickname + "\n").encode('utf-8'))
                    # self.refreshMenu()      
                elif message.split(":")[0] == "USERLIST":
                    if message[-1] == ":":
                        clientui.users_list.clear()
                        clientui.create_group_list.clear()
                        clientui.manage_group_list.clear()
                    else:
                        users = message.split(":")[1].split(",")
                        clientui.users_list.clear()
                        clientui.create_group_list.clear()
                        clientui.manage_group_list.clear()
                        for user in users:
                            if user not in chat_history:
                                chat_history[user] = []
                            item = QListWidgetItem()
                            item.setText(f"{user}")
                            clientui.users_list.addItem(item)
                            item2 = QListWidgetItem()
                            item2.setText(f"{user}")
                            clientui.create_group_list.addItem(item2)
                            item3 = QListWidgetItem()
                            item3.setText(f"{user}")
                            clientui.manage_group_list.addItem(item3)
                elif message.split(":")[0] == "GROUPLIST":
                    if message[-1] == ":":
                        clientui.groups_list.clear()
                    else:
                        groups = message.split(":")[1].split(",")
                        clientui.groups_list.clear()
                        for gr in groups:
                            if gr not in group_history:
                                group_history[gr] = []
                            item = QListWidgetItem()
                            item.setText(f"{gr}")
                            clientui.groups_list.addItem(item)
                elif message.split(":")[0] == "USERTXT":
                    sender = message.split(":",2)[1]
                    chat_history[sender].append(sender+":"+ message.split(":",2)[2]+"\n")
                    if self.reciever != "":
                        clientui.messages_box.setText("".join(chat_history[self.reciever]))
                        #refresh seen status
                        if self.ui.stacked_widget.currentIndex() == clientui.views["chat"]:
                            self.client.send(("USERINFO:"+self.reciever+"\n").encode("utf-8")) 
                elif message.split(":")[0] == "GROUPTXT":
                    sender = message.split(":")[2]
                    group_name= message.split(":")[1]
                    group_history[group_name].append(sender+":"+ message.split(":")[3]+"\n")
                    if self.group != "":
                        clientui.group_messages_box.setText("".join(group_history[self.group]))
                        # #refresh seen status
                        if self.ui.stacked_widget.currentIndex() == clientui.views["group"]:
                            self.client.send(("GROUPINFO:"+self.group+"\n").encode("utf-8")) 
                elif message.split(":")[0] == "USERINFO":
                    status_ = message.split(":")[2]
                    clientui.chat_label.setText(f"[{self.reciever}] {status_}")
                elif message.split(":")[0] == "GROUPINFO":
                    role_ = message.split(":")[2]
                    clientui.group_chat_label.setText(f"Group [{self.group}] role: {role_}")
                    clientui.cur_groups_members.clear()
                    for memb in (message.split(":")[3]).split(","):
                        item = QListWidgetItem()
                        item.setText(f"{memb}")
                        clientui.cur_groups_members.addItem(item)
                       
                        for i in range( clientui.manage_group_list.count()):
                            item2 = clientui.manage_group_list.item(i)
                            if memb == item2.text():
                                item2.setSelected(True)

                    if role_ == "Admin":
                        clientui.manage_button.setVisible(True)
                    else:
                        clientui.manage_button.setVisible(False)
                elif message.split(":")[0] == "USERSEEN":
                    sender = message.split(":",2)[1]
                    while "(SEEN)\n" in chat_history[sender]:
                        chat_history[sender].remove("(SEEN)\n")
                    chat_history[sender].append("(SEEN)\n")
                    if self.reciever != "":
                        clientui.messages_box.setText("".join(chat_history[self.reciever]))
                elif message.split(":")[0] == "GROUPSEEN":
                    #GROUPSEEN:GRPNAME:USER
                    group_name = message.split(":",2)[1]
                    seen_by_who = message.split(":",2)[2]
                    while f"(SEEN by {seen_by_who})\n" in group_history[group_name]:
                        group_history[group_name].remove(f"(SEEN by {seen_by_who})\n")
                    group_history[group_name].append(f"(SEEN by {seen_by_who})\n")
                    if self.group != "":
                        clientui.group_messages_box.setText("".join(group_history[self.group]))
                elif message.split(":")[0] == "GROUPCHANGE":
                    if message.split(":")[2] in group_history:
                        group_history[message.split(":")[1]] = group_history[message.split(":")[2]]
                        if message.split(":")[1] != message.split(":")[2]:
                            group_history[message.split(":")[2]] = []
        except:
            # Close Connection When Error
            self.ui.showError("Connection ended")
            self.client.close()
            # break

            
    def go_to_chat(self, item):
        self.reciever = item.text()
        self.client.send(("USERINFO:"+self.reciever+"\n").encode("utf-8"))
        self.ui.show_view(clientui.views["chat"])
        clientui.messages_box.setText("".join(chat_history[self.reciever]))
               
    def go_to_Groupchat(self, item):
        self.group = item.text()
        self.client.send(("GROUPINFO:"+self.group+"\n").encode("utf-8"))
        self.ui.show_view(clientui.views["group"])
        clientui.group_messages_box.setText("".join(group_history[self.group]))
    def send_text(self, text):
        timestamp = QDateTime.currentDateTime().toString(Qt.ISODate)
        self.client.send(("USERTXT:"+self.reciever+":"+text+f"[{timestamp}]"+"\n").encode("utf-8"))
        chat_history[self.reciever].append(self.nickname+":"+text+f"[{timestamp}]"+"\n")
        clientui.messages_box.setText("".join(chat_history[self.reciever]))
        clientui.chat_box.clear()
    def send_group_text(self, text):
        timestamp = QDateTime.currentDateTime().toString(Qt.ISODate)
        self.client.send(("GROUPTXT:"+self.group+":"+text+f"[{timestamp}]"+"\n").encode("utf-8"))
        group_history[self.group].append(self.nickname+":"+text+f"[{timestamp}]"+"\n")
        clientui.group_messages_box.setText("".join(group_history[self.group]))
        clientui.group_chat_box.clear()
        

if __name__ == "__main__":
    client = Client()
    
