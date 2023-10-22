# Socket-Messager


A server client application for a chat system with an intuitive GUI built using PyQt5.

## Features


- Supports both IPv4 and IPv6 client connections.
![Screenshot (8)](https://github.com/eralds/Socket-Messager/assets/94328315/dae73c61-ece0-41cb-ad58-f7b514062e05)
- Uses a simple protocol with commands such as `STATUS:ONLINE`, `USERTXT`, `GROUPTXT`, `CREATEGROUP`, etc.
- Real-time client status updates in the GUI.
![Screenshot (9)](https://github.com/eralds/Socket-Messager/assets/94328315/06dd563a-8e34-42c6-b409-a9dfa11e5dff)
- Buffering of messages for offline users.
- Last seen functionality for users.
![Screenshot (11)](https://github.com/eralds/Socket-Messager/assets/94328315/17e2a79a-360a-46a1-b01b-1bec954ad850)
- Group chat feature with group management (creation, members addition/removal).
- Connection handling with threading to support multiple simultaneous clients.
- Supports querying user and group information.
![Screenshot (10)](https://github.com/eralds/Socket-Messager/assets/94328315/289c98fd-8210-427d-bcc2-d18fd6a6b0e0)








## Requirements

- Python 3.x
- PyQt5

## Usage

1. Ensure you have the necessary libraries installed.
    ```bash
    pip install PyQt5
    ```

2. Run the server.
    ```bash
    python server.py
    ```

3. Run the client.
    ```bash
    python client.py
    ```
