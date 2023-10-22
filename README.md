# Socket-Messager


A server client application for a chat system with an intuitive GUI built using PyQt5.

## Features

- Supports both IPv4 and IPv6 client connections.
- Uses a simple protocol with commands such as `STATUS:ONLINE`, `USERTXT`, `GROUPTXT`, `CREATEGROUP`, etc.
- Real-time client status updates in the GUI.
- Buffering of messages for offline users.
- Group chat feature with group management (creation, members addition/removal).
- Connection handling with threading to support multiple simultaneous clients.
- Last seen functionality for users.
- Supports querying user and group information.

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

3. Run the server.
    ```bash
    python client.py
    ```
