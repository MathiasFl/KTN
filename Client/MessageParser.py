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
        payload = json.loads(payload)
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return 'Response not valid \n'

    def parse_error(self, payload):
        tempString = payload.get('timestamp') + ' \n\t'
        tempString += payload.get('response') + ': \t'
        tempString += payload.get('content') + '\n'
        return tempString

    def parse_info(self, payload):
        tempString = payload.get('timestamp') + ' '
        tempString += payload.get('content') + '\n'
        return tempString

    # Include more methods for handling the different responses...

    def parse_message(self, payload):
        tempString = payload.get('timestamp') + ' '
        tempString += payload.get('sender') + ': \t'
        tempString += payload.get('content') + '\n'
        return tempString

    def parse_history(self, payload):
        tempArray = payload.get('content')
        tempString = ''
        for replies in tempArray:
            tempString += self.parse_message(json.loads(replies))
        return tempString
