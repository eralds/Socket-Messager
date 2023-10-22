import threading
import socket
import serverui
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from datetime import datetime, timedelta

HOST = "localhost"
port = 8081

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.bind((HOST, port))
cs.listen()
csv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
csv6.bind((HOST, port))
csv6.listen()
app = QApplication(sys.argv)
win = serverui.ServerUI()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host,port))
# server.listen()

# server commands
# STATUS:ONLINE
# USERTXT:USER_NAME:msg
# GROUPTXT:GROUP_NAME:msg
# CREATEGROUP:GROUPNAME:NICK1, NICK2, NICK3
# REMOVE:GROUP_NAME:USER1
# NICK:NICKNAME
# TEXTSEEN
# GROUPSEEN


# client commands
# USERTXT:SENDER:msg
# GROUPTXT:SENDER:msg
# ERROR:msg
# LEFT:USER
# USERINFO:ON/OFF:LASTTIME
# USERSEEN:USERNAME
# GROUPSEEN:GROUPNAME:USERNAME

#keeps track of all clients in form nickname => client
clients = {}
#keeps track of status of each client; client => true or false
status = {}
#keeps track of group members; group_name => (admin,[memb1, memb2 etc.])
group = {}
#list of buffered messages for each member; client => ["msg1", "msg2"]
buffered = {}

handlers = {}
#keeps the time that a particular has last turned offline; nickname => ISO
last_seen = {}

def iso_to_minutes_ago(iso_timestamp):
    parsed_time = iso_timestamp
    time_diff = datetime.now() - parsed_time
    minutes_diff = int(time_diff.total_seconds() / 60)
    return f"{minutes_diff} minutes ago"

# def broadcast(message): 
#     for client in clients:
#         client.send(message)
        
def emptyBuffer(nickname): 
    client = clients[nickname]
    for msg in buffered[client]:
        sendTo(client,nickname,msg)
    buffered[client] = []
    
def sendTo(reciever, sender, message):
    if status[reciever] == True:
        reciever.send((message+"\n").encode("utf-8"))
        #he is not save buffer
    else:
        buffered[reciever].append(message)

def sendGroup(group_name, sender, rawmsg):
    for memb in (group[group_name][1] + [group[group_name][0]]):
        if memb != sender:
            sendTo(clients[memb], sender, ("GROUPTXT:" + group_name+ ":" + sender +":"+rawmsg ))
            
def updateLists():
    keys = [ key for key in clients.keys()]
    for key_ in keys:
        sendTo(clients[key_], clients[key_], "USERLIST:" + ",".join([nick for nick in keys if nick != key_]))
        groups_ = [ key for key in group.keys()]
        sendTo(clients[key_], clients[key_], "GROUPLIST:" + ",".join([nick for nick in groups_ if key_ in (group[nick][1] + [group[nick][0]]) ]))
    
def handle(win,tp):
    nickname,msgs = tp
    client = clients[nickname]
    for msg in msgs.split("\n"):
        message = msg.split(":", 2)

        if message[0] == "STATUS":
            if message[1] == "ONLINE":
                status[client] = True
                emptyBuffer(nickname)
                win.set_client_status(nickname, True)

            else:
                status[client] = False
                win.set_client_status(nickname, False)
                last_seen[nickname] = datetime.now()
                
                
        elif status[client]:
            if message[0] == "USERTXT":
                to = clients[message[1]]
                sendTo(to, nickname, "USERTXT:" + nickname + ":" + message[2])
                #the person we are sending to is online

            elif message[0] == "GROUPTXT":
                sendGroup(message[1], nickname, message[2])
            elif message[0] == "USERLIST":
                keys = [ key for key in clients.keys()]
                sendTo(client, client, "USERLIST:" + ",".join([nick for nick in keys if nick != nickname]))
                print("USERLIST:" + ",".join([nick for nick in clients if nick != nickname]))
            elif message[0] == "GROUPLIST":   
                keys = [ key for key in group.keys()]
                sendTo(client, client, "GROUPLIST:" + ",".join([nick for nick in keys if nickname in (group[nick][1] + [group[nick][0]]) ]))
            elif message[0] == "USERINFO":
                sendTo(clients[message[1]],client, "USERSEEN:"+nickname)
                if status[clients[message[1]]]:
                    sendTo(client, client, "USERINFO:"+message[1]+":ONLINE")
                else:
                    sendTo(client, client, "USERINFO:"+message[1]+":Last seen " + iso_to_minutes_ago(last_seen[message[1]]))
            elif message[0] == "GROUPINFO":
                if message[1] in group:
                    for mem in (group[message[1]][1]+[group[message[1]][0]]):  
                        sendTo(clients[mem],client, "GROUPSEEN:"+message[1]+":"+nickname)
                    if nickname == group[message[1]][0]:
                        sendTo(client, client, "GROUPINFO:"+message[1]+":Admin:"+",".join([group[message[1]][0] + " (Admin)"] + group[message[1]][1]))
                    else:
                        sendTo(client, client, "GROUPINFO:"+message[1]+":User:"+",".join([group[message[1]][0] + " (Admin)"] + group[message[1]][1]))
                    
                    # sendTo(client, client, "USERINFO:"+message[1]+":Last seen " + iso_to_minutes_ago(last_seen[message[1]]))
            
            elif message[0] == "CREATEGROUP":
                group[message[1]] = (nickname, message[2].split(","))
                updateLists()
            elif message[0] == "MANAGEGROUP":
                group[msg.split(":")[2]] = group.pop(msg.split(":")[1])
                group[msg.split(":")[2]] = ( group[msg.split(":")[2]][0], (msg.split(":")[3]).split(","))
                newgrpname = msg.split(":")[2]
                updateLists()
                if group[newgrpname][1][0] != "":
                    for mem in (group[newgrpname][1]+[group[newgrpname][0]]):  
                        sendTo(clients[mem],client, "GROUPCHANGE:"+msg.split(":")[2]+":"+msg.split(":")[1])
                else: 
                    for mem in ([group[newgrpname][0]]):  
                        sendTo(clients[mem],client, "GROUPCHANGE:"+msg.split(":")[2]+":"+msg.split(":")[1])
                
                
def conEnded(win, nickname):
    client = clients[nickname]
    clients.pop(nickname)
    status.pop(client)
    buffered.pop(client)
    client.close()
    win.remove_client(nickname)
    print(f"{nickname} left the chat")
    updateLists()
    
def recieve(win, tp):
    nickname, client = tp
    clients[nickname] = client
    win.add_client(nickname)
    buffered[client] = []
    status[client] = True
    updateLists()
    handlers[nickname] = Handler(client)
    handlers[nickname].messageReceived.connect(lambda msg: handle(win, (nickname,msg)))
    handlers[nickname].connectionEnded.connect(lambda: conEnded(win, nickname))
    handlers[nickname].start()
        
def main():
    
    # socket_.newConnection.connect(lambda tp: recieve(win, tp))
    # recieve(win)
    reciver_4 = Reciever(cs)
    reciver_4.newConnection.connect(lambda tp: recieve(win, tp))
    reciver_4.connectionEnded.connect(lambda n: conEnded(win,n))
    reciver_4.start()
    reciver_6 = Reciever(csv6)
    reciver_6.newConnection.connect(lambda tp: recieve(win, tp))
    reciver_6.connectionEnded.connect(lambda n: conEnded(win,n))
    reciver_6.start()
        # socket_.messageReceived.connect(lambda msg: handle(win,msg))
        # # socket_.connectionEnded.connect(lambda: conEnded(win, nickname))
        # socket_.start()
    # thread = threading.Thread(target=recieve, args=(win,))
    # thread.start()
    win.show()
    sys.exit(app.exec_())
       
class Handler(QtCore.QThread):
    # newConnection = QtCore.pyqtSignal(object)
    messageReceived = QtCore.pyqtSignal(object)
    connectionEnded = QtCore.pyqtSignal()
    def __init__(self, client):
        super().__init__()
        # self.port = port
        self.client= client

    def run(self):
        while True:
            try:
                msg = self.client.recv(1024).decode("utf8")
                self.messageReceived.emit(msg)
            except Exception as e:
                print(str(e))
                self.connectionEnded.emit()
                break
                # self.connectionEnded.emit(True)
                

class Reciever(QtCore.QThread):
    newConnection = QtCore.pyqtSignal(object)
    # messageReceived = QtCore.pyqtSignal(object)
    connectionEnded = QtCore.pyqtSignal(object)
    def __init__(self,socket):
        super().__init__()
        self.socket = socket
        # self.port = port
        # self.client= client

    def run(self):
        while True:
            try:
                
                client, address = self.socket.accept()
                print("Connected with {}".format(str(address)))
                # Request And Store Nickname
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8').split("\n")[0].split(":")
                nickname = nickname[1]
                # clients.append(client
                # Print And Broadcast Nickname
                print("Nickname is {}".format(nickname))
               
                self.newConnection.emit((nickname, client))
            except Exception as e:
                self.connectionEnded.emit(nickname)
                break
            

           
if __name__ == "__main__":
    main()
    