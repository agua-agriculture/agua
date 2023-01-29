from fastapi import FastAPI, Request
from messages import Messenger

server = FastAPI()
messenger = Messenger()

@server.get("/")
def healthcheck():
    """Returns a 200 OK response if the server is running."""
    return {"status": "200"}

@server.route("/sms")
def sms(request: Request):
    """Handles incoming SMS messages from Twilio.
    
    """
    # Get the message body and phone number from the request
    body = request.form.get("Body")

    # Check if the message is a subscription request
    if body.lower() == "subscribe":
        # Subscribe the phone number to the messaging service
        messenger.subscribe(request.form.get("From"))
    elif body.lower() == "unsubscribe":
        # Unsubscribe the phone number from the messaging service
        messenger.unsubscribe(request.form.get("From"))
    else:
        # Handle the message
        pass

    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    pass