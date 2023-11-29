
import os
from tars_vision import LTM
import json
from twilio.rest import Client
from typing import Tuple, List

class TarsTextHandler:
    def __init__(self, twilio_account_sid, twilio_auth_token, phone_number, ltm_instance):
        """
        Initializes TarsTextHandler with Twilio credentials, phone number, and an instance of the LTM class.

        """
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.phone_number = phone_number
        self.ltm = ltm_instance
        self.conversations_path = "conversations" 
    def send_text(self, to_number, message):
        """
        Sends a text message to the specified phone number.
        """
        message = self.client.messages.create(
            body=message,
            from_=self.phone_number,
            to=to_number
        )
        return message.sid

    def handle_incoming_text(self, from_number, message_body, caller_name):
        """
        Handles incoming text messages and updates the conversation history.

        """
        # Update the conversation file with the inbound message
        self.update_conversation_file(from_number, message_body)

        # Process and store the text in the LTM class
        self.ltm.store_dialogue_turn(message_body, "")
        # Additional AI-based processing and response generation

    def update_conversation_file(self, phone_number, message):
        """
        Updates or creates a conversation file for the specified phone number.

        """
        file_path = os.path.join(self.conversations_path, f"{phone_number}.json")
        if not os.path.exists(self.conversations_path):
            os.makedirs(self.conversations_path)

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                conversation = json.load(file)
        else:
            conversation = {"phone_number": phone_number, "conversation": []}

        conversation["conversation"].append(message)

        with open(file_path, 'w') as file:
            json.dump(conversation, file, indent=4)





import faiss
import numpy as np
import openai
import os
import pickle
from flask import Flask, request




api_key = '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'  
ltm = LTM(api_key=api_key)


twilio_account_sid = 'SK9981340905e59767b1a479726d299ddd'
twilio_auth_token = 'zIvtJV7nPVKcz6CJVVEk9dfF9J9KNncM'  
phone_number = '8557520721'  
tars_handler = TarsTextHandler(
    twilio_account_sid=twilio_account_sid,
    twilio_auth_token=twilio_auth_token,
    phone_number=phone_number,
    ltm_instance=ltm
)




app = Flask(__name__)

@app.route("/sms_webhook", methods=['GET', 'POST'])
def sms_webhook():
    from_number = request.values.get('From', None)
    message_body = request.values.get('Body', None)

    
    
    caller_name = "User"  # Replace with actual caller name

    
    
    tars_handler.handle_incoming_text(from_number, message_body, caller_name)
    print(from_number, message_body)

    return "SMS Received", 200

@app.route("/", methods=["GET"])
def index(): # Goes under flask
    print("index")
    return "TARS phone system is running"
app.config['WTF_CSRF_ENABLED'] = False

if __name__ == "__main__":
    app.run(debug=True)





