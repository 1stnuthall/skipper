# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from datetime import date

from utils import sendMessage
from views import *
from config import *

from .config import *
from .osm import OSM

def send_text_message(section, user, message):
  twilio = Client(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)
  recipients = [number for id, contact in OSM(section).scouts_contacts().items() for number in contact['text_messages']]
  for recipient in recipients:
    try:
      twilio_message = twilio.messages.create(
        body=message,
        to=recipient,
        messaging_service_sid=TWILIO_MESSAGE_SERVICE,
      )

    except:
      print(f"Failed: {twilio_message.body}")
      sendMessage(
        channel = user,
        text = f"Text Message Failed: {twilio_message.body}"
    )

###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_text_message = dict(
    group = "Section",
    title_popup = "Send Text Message",
    title_home = "Send Text Message",
    action_id = "req_text_message",
    action = "send_text_message",
    command = "sms",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
        BLK_MESSAGE
    ]
)

OPS_REQUESTS.update(req_text_message=req_text_message)

@app.action("req_text_message")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_text_message['title_popup'],
        req_blocks = req_text_message['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_text_message",
    )


@app.view("req_text_message")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    message = body['view']['state']['values']['message']['value']
    user = body['user']['id']
    ack()
    send_text_message(section = section, user = user, message = message)
    