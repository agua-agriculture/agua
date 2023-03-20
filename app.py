import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from dotenv import load_dotenv
import openai

# Load the environment variables
load_dotenv()

# Twilio variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_MESSAGING_SERVICE_ID = os.getenv("TWILIO_MESSAGING_SERVICE_ID")

# Initilize the twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample data
sample_data = [{
    "phone": "+12899716341",
    "crop": "wheat",
    "acres": "100",
    "irrigation_type": "drip",
}]

# Initialize the flask app
app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    message_body = request.form['Body']
    from_number = request.form['From']

    # Parse the message body to get the crop and acres
    crop, acres, irrigation_type = message_body.split(", ")

    farmer = {}
    # Process and store the crop data in the database
    farmer["phone"] = from_number
    farmer["crop"] = crop
    farmer["acres"] = acres
    farmer["irrigation_type"] = irrigation_type

    sample_data.append(farmer)

    response = MessagingResponse()
    response.message("Crop data received. You'll get irrigation recommendations soon.")
    return str(response)


@app.route('/send-recommendations', methods=['POST'])
def send_recommendations():
    # Retrieve the data from the database for the farmers

    for farmer in sample_data:
        # Generate irrigation recommendations using OpenAI API
        prompt = f"Generate irrigation recommendations for {farmer['crop']} on {farmer['acres']} acres."
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