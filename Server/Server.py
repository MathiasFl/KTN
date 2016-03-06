# -*- coding: utf-8 -*-
import SocketServer
import json

clients = []

usersonline = []

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

helpMenu = "Following commands are available \n" \
           "login <username>\t-\tlog in with the given username" \
           "msg <message>\t-\tsend message\nnames\t-\tlist users in chat" \
           "help\t-\tview help text\n"


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        client_name = ''
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            recv_data = self.connection.recv(4096)
            if recv_data:
                json_data = json.loads(recv_data)
                logged_inn = self in clients
                if json_data.get('request') == 'login':
                    if logged_inn:
                        reply = {
                            'response': 'message',
                            'error': 'Logout before trying to login with a new name'
                        }
                        self.send(reply)
                    else:
                        client_name = self.login(json_data.get('message'))
                elif json_data.get('request') == 'message':
                    if logged_inn:
                        reply = {
                            'response': 'message',
                            'message': client_name + ":\t" + json_data.get('message')
                        }
                        self.broadcast(reply)
                    else:
                        reply = {
                            'response': 'message',
                            'error': 'You must be logged inn to send messages'
                        }
                        self.send(reply)
                elif json_data.get('request') == 'logout':
                    self.logout(client_name)
                elif json_data.get('request') == 'help':
                    reply = {
                        'response': 'message',
                        'message': helpMenu
                    }
                    self.send(reply)

    def login(self, username):
        if username not in usersonline:
            clients.append(self)
            usersonline.append(username)
            reply = {
                'response': 'login',
                'username': username
            }
        else:
            reply = {
                'response': 'login',
                'error': 'Name already taken!',
                'username': username
            }
        self.send(reply)
        return username

    def send(self, json_data):
        self.connection.sendall(json_data)

    @staticmethod
    def broadcast(reply):
        for client in clients:
            client.send(reply)

    def logout(self, username):
        if username in usersonline:
            reply = {
                'response': 'logout'
            }
            clients.remove(self)
            usersonline.remove(username)
        else:
            reply = {
                'response': 'logout',
                'error': 'Not logged inn'
            }
        self.send(reply)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
