# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        
        messageReceiver = MessageReceiver(self,self.connection)
        messageReceiver.run()
        
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        MessageReceiver(self.host, self.server_port)

    def disconnect(self):
        self.connection.close()
        pass

    def receive_message(self, message):
        print MessageParser.parse(message)
        pass

    def send_payload(self, data):
        self.connection.send(data)
        pass

    def getUserInput(self):
        userInput = raw_input()
        if userInput.lower() == "help" or userInput.lower() == "names" or userInput.lower() == "logout":
            self.json_Encoder(userInput.lower(), "None")
        elif userInput[:5].lower() == "login":
            self.json_Encoder(userInput[:5], userInput[6:])
        elif userInput[:3].lower() == "msg":
            self.json_Encoder(userInput[:3], userInput[4:])
        else:
            print "No valid input try again:\n"

    def json_Encoder(self, request, content):
        self.send_payload(json.dump({'request': request, 'content': content}))
        # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
