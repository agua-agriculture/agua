from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

class Messenger:

    def __init__(self, db) -> None:
        self.client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), 
                             os.environ.get("TWILIO_AUTH_TOKEN"))
        self.from_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self.db = db

    def send_message(self, to_number: str, message: str) -> None:
        """Sends a message to a phone number.
        This function will be called by the API to send messages to subscribers.
        """
        self.client.messages.create(to=to_number, 
            from_=self.from_number, 
            body=message,
            messaging_service_sid=os.environ.get("TWILIO_MESSAGING_SERVICE_SID")
        )

    def subscribe(self, to_number: str) -> None:
        """Subscribes a phone number to the messaging service.
        
        This will be the first function checked in the /sms route of the API.
        """

        # Subscribe a phone number to a messaging service
        self.client.messaging.services(os.environ.get("TWILIO_MESSAGING_SERVICE_SID")) \
            .phone_numbers(to_number).create()

    def unsubscribe(self, to_number: str) -> None:
        """Unsubscribes a phone number from the messaging service.
        
        This will be the second function checked in the /sms route of the API.
        """

        # Unsubscribe a phone number from a messaging service
        self.client.messaging.services(os.environ.get("TWILIO_MESSAGING_SERVICE_SID")) \
            .phone_numbers(to_number).delete()

    def handle_message(self, request):
        """
        """
        pass