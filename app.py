import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
# from dotenv import load_dotenv
import openai
from weather import Weather

# Load the environment variables
# load_dotenv()

# Twilio variables
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
TWILIO_MESSAGING_SERVICE_ID = os.environ["TWILIO_MESSAGING_SERVICE_ID"]

# Initilize the twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Sample data
sample_data = [{
    "phone": "+12899716341",
    "location": "goias",
    "crop": "wheat",
    "acres": "100",
    "irrigation_type": "drip",
}]

# Initialize the flask app
app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return {"status": 200}

@app.route('/sms', methods=['POST'])
def sms():
    message_body = request.form['Body']
    from_number = request.form['From']

    # Check if the user wants an update
    if message_body.lower() == "update":
        send_recommendations()
        return "Recommendations sent!"
    
    # Parse the message body to get the crop and acres
    msg = message_body.split(", ")
    if len(msg) != 4:
        response = MessagingResponse()
        response.message("Invalid message format. Please send the message in the following format: location, crop, acres, irrigation_type")
        return str(response)
    else:
        location, crop, acres, irrigation_type = msg

    # Store the data in a database
    farmer = {}

    # Process and store the crop data in the database
    farmer["phone"] = from_number
    farmer["location"] = location
    farmer["crop"] = crop
    farmer["acres"] = acres
    farmer["irrigation_type"] = irrigation_type

    # Add the data to the db
    sample_data.append(farmer)

    response = MessagingResponse()
    response.message("Crop data received. You'll get irrigation recommendations soon.")
    return str(response)


@app.route('/send-recommendations', methods=['POST'])
def send_recommendations():

    for farmer in sample_data:
        # Retrieve the data from the database for the farmers
        monitor = Weather(farmer["location"])
        required_irrigation = monitor.get_total_irrigation(farmer["crop"], farmer["acres"])

        # Generate irrigation recommendations using OpenAI API
        prompt = f"""
            Generate irrigation recommendations for {farmer['crop']} on {farmer['acres']} acres. 
            The total irrigation is {required_irrigation} mm.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )

        recommendation = response.choices[0].text.strip()

        # Send SMS with the recommendations
        client.messages.create(
            body=recommendation,
            from_=TWILIO_PHONE_NUMBER,
            to=farmer["phone"],
        )

    return "Recommendations sent!"


@app.route('/stop-messaging', methods=['POST'])
def stop_messaging():
    from_number = request.form['From']

    # Remove farmer's number from the database
    for farmer in sample_data:
        if farmer["phone"] == from_number:
            sample_data.remove(farmer)

    response = MessagingResponse()
    response.message("You have been unsubscribed from the irrigation recommendations.")
    return str(response)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))