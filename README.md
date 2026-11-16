# LAN Chat App

A simple multi-user chat application for a local network, built with Python's `socket` and `threading` modules. One computer runs the server, and any number of others connect as clients and chat in real time from the terminal.

## Features

- Multiple clients chatting at the same time
- Nickname for every user
- Messages from one user are broadcast to everyone else
- Join and leave notifications
- Works on one computer (localhost) or across a LAN
- Pure Python standard library, so there is nothing to install

## How It Works

The app uses a **client-server model over TCP**.

```
 Client A ──┐                      ┌── Client B
            ├──►   Server   ──────►┤
 Client C ──┘   (broadcasts)       └── Client D
```

### Server (`server.py`)

| Function | Purpose |
|---|---|
| `receive_connections()` | Waits for new clients, asks each for a nickname, announces the join, and starts a thread for the client |
| `handle_client(client)` | Runs in its own thread per client. Receives messages and passes them to `broadcast()`. Cleans up when the client leaves |
| `broadcast(message, client_socket)` | Sends a message to every connected client except the sender |

The server keeps two lists, `clients` (sockets) and `nicknames`, which are matched by position.

### Client (`client.py`)

| Function | Purpose |
|---|---|
| `receive()` | Runs in a thread. Prints incoming messages and replies to the server's `NICK` request with the user's nickname |
| `write()` | Runs in a thread. Reads what the user types and sends it as `nickname: message` |

### Message flow

1. The client connects to the server.
2. The server sends `NICK`, and the client replies with its nickname.
3. The server announces `<nickname> joined the chat!` to the others.
4. When a user types a message, `write()` sends it to the server.
5. The server's `handle_client()` receives it and `broadcast()` forwards it to everyone else.
6. Each other client's `receive()` prints it.
7. If a client disconnects, the server announces `<nickname> left the chat!`.

## Requirements

- Python 3.6 or newer
- All computers on the same local network (for LAN use)

## Getting Started

### 1. Start the server

On the computer that will host the chat:

```bash
python server.py
```

You should see:

```
Server is running... Waiting for connections.
```

### 2. Find the server's IP address (LAN use only)

On the server computer:

- **Windows:** run `ipconfig` and look for the *IPv4 Address*
- **Linux / macOS:** run `ip a` or `ifconfig` and look for an address like `192.168.x.x`

### 3. Start a client

On each user's computer:

```bash
python client.py
```

When prompted, enter a nickname and the server's IP address. Press Enter without typing an IP to connect to the same computer (`127.0.0.1`).

### 4. Chat

Type a message and press Enter. Everyone else sees it as `nickname: message`.

To quit, press `Ctrl+C`.

## Configuration

| Setting | Where | Default |
|---|---|---|
| Port | `port` in `server.py` and the port in `client.py` | `5000` |
| Listen address | `host` in `server.py` | `0.0.0.0` (all network interfaces) |

The port must match in both files.

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `ConnectionRefusedError` | The server isn't running, or the IP or port is wrong |
| Client on another computer can't connect | Wrong IP entered, or the server's firewall is blocking port 5000. Allow it through the firewall |
| `Address already in use` when restarting the server | The old socket is still closing. Wait about a minute, or change the port |
| Computers are on different networks | Both must be on the same LAN, or reachable by the IP you enter |

## Known Limitations

This is a learning project, and it has some simplifications:

- No encryption, so messages are sent as plain text. Use it on trusted networks only.
- No private messages or
