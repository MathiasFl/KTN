#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import json
import datetime
import re

# Change to increase or decrease max num of messages in history
HISTORY_CAP = 10

clients = []

usersonline = []

history = []

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

helpMenu = "\n\tFollowing commands are available \n" \
           "\tlogin <username>\t-\tlog in with the given username\n" \
           "\tmsg <message>\t-\tsend message\n\tnames\t-\tlist users in chat" \
           "\n\thelp\t-\tview help text\n"


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
                print json_data
                if json_data.get('request') == 'login':
                    if logged_inn:
                        reply = {
                            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                            'sender': 'server',
                            'response': 'error',
                            'content': 'Logout before trying to login with a new name'
                        }
                        self.send(reply)
                    else:
                        client_name = self.login(json_data.get('content'))
                elif json_data.get('request') == 'msg':
                    if logged_inn:
                        reply = {
                            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                            'sender': client_name,
                            'response': 'message',
                            'content': json_data.get('content')
                        }
                        history.append(json.dumps(reply))
                        self.broadcast(reply)
                    else:
                        reply = {
                            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                            'sender': 'Server',
                            'response': 'error',
                            'content': 'You must be logged inn to send messages'
                        }
                        self.send(reply)
                elif json_data.get('request') == 'names':
                    if logged_inn:
                        reply = {
                            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                            'sender': 'server',
                            'response': 'info',
                            'content': self.get_names()
                        }
                        self.send(reply)
                    else:
                        reply = {
                            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                            'sender': 'Server',
                            'response': 'error',
                            'content': 'You must be logged inn to view online users'
                        }
                        self.send(reply)

                elif json_data.get('request') == 'logout':
                    self.logout(client_name)
                elif json_data.get('request') == 'help':
                    reply = {
                        'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                        'sender': 'Server',
                        'response': 'info',
                        'content': helpMenu
                    }
                    self.send(reply)

    def get_names(self):
        listofnames = ''
        for x in range(0, len(usersonline) - 1):
            listofnames += usersonline[x] + ", "
        listofnames += usersonline[len(usersonline) - 1]
        return listofnames

    def login(self, username):
        invaldregex = re.compile('\W')
        username = username.encode("utf-8")
        if not invaldregex.match(username):
            if username not in usersonline and len(username) >= 2:
                login = {
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'sender': 'Server',
                    'response': 'info',
                    'content': username + ' just logged in, welcome him!'
                }
                self.broadcast(login)  # Send Login message to all users
                clients.append(self)
                usersonline.append(username)
                reply = {
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'sender': 'Server',
                    'response': 'info',
                    'content': 'You just logged inn with ' + username
                }
                self.send_history()
            else:
                reply = {
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'sender': 'Server',
                    'response': 'error',
                    'content': username + ' is already taken!',
                }
            self.send(reply)
            return username
        else:
            reply = {
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                'sender': 'Server',
                'response': 'error',
                'content': 'Invalid username: ' + username
            }
            self.send(reply)

    def send(self, response):
        json_data = json.dumps(response)
        self.connection.sendall(json_data)

    @staticmethod
    def broadcast(reply):
        for client in clients:
            client.send(reply)

    def logout(self, username):
        if username in usersonline:
            reply = {
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                'sender': 'Server',
                'response': 'info',
                'content': 'You are now logged out, come back again soon'
            }
            clients.remove(self)
            usersonline.remove(username)
        else:
            reply = {
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                'sender': 'Server',
                'response': 'error',
                'content': 'Not logged inn'
            }
        self.send(reply)

    def send_history(self):
        # caping history
        while len(history) > HISTORY_CAP:
            history.pop(0)
        reply = {
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
            'sender': 'Server',
            'response': 'history',
            'content': history
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
    HOST, PORT = '10.20.86.75', 30000
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
