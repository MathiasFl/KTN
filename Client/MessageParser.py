import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,

	    # More key:values pairs are needed
        }

    def parse(self, payload):
        payload = # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
        	
            return 'Response not valid \n'

    def parse_error(self, payload):
        tempString = payload.get('timestamp') + ' '
        tempString += 'Sender: ' + payload.get('sender') + ' '
        tempString += payload.get('response') + ': '
        tempString += payload.get('error') + '\n'
        return tempString

    def parse_info(self, payload):
        tempString = payload.get('timestamp') + ' '
        tempString += payload.get('info') + ': '
        tempString += payload.get('message') + '\n'
        return tempString
    # Include more methods for handling the different responses...

    def parse_message(self, payload):
        tempString = payload.get('timestamp') + ' '
        tempString += payload.get('sender') + ': \t'
        tempString += payload.get('message') + '\n'
        return tempString

    def parse_history(self, payload):
        tempArray = payload.get('history')
        for replies in tempArray:
            tempString += parse_message(replies) + '\n'

        return tempArray
