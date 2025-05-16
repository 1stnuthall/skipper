# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from datetime import date

from utils import sendMessage
from views import *
from config import *

from .config import *
from .osm import OSM

from slack_bolt import App, Say, Fail, Complete

def get_evening(section, date):
    for programme in section.get_programme_summary()['items']:
        if programme['meetingdate'] == date:
            return programme
        

def get_programme(section, date):
  evening_id = get_evening(section, date)['eveningid']
  url = f"{OSM_BASE_URL}/ext/programme/?action=printProgramme&risks=1&sectionid={section.id}&eveningid={evening_id}"
  try:
    programme = section.get(url = url, json_output=False)
    return programme.content
  except:
    return "No programme found"

###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_get_programme = dict(
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

OPS_REQUESTS.update(req_text_message=req_get_programme)

@app.action("req_get_programme")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_get_programme['title_popup'],
        req_blocks = req_get_programme['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_get_programme",
    )


@app.view("req_get_programme")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    message = body['view']['state']['values']['message']['value']
    user = body['user']['id']
    ack()
    get_programme(section = section, user = user, message = message)
    
# This sample custom step formats an input and outputs it
@app.function("req_get_programme")
def display_programme(inputs: dict, fail: Fail, complete: Complete):
    try:
        section = OSM("beavers")
        summary = get_evening(section, "2025-03-13")
        content = get_programme(section = "beavers", date = "2025-03-13")        
        message_blocks = [
           HeaderBlock(
                text = f"Session Plan for {summary['meetingdate']}",   
                emoji = True
            ),
            SectionBlock(
                text = f"Please check the plan to identify if any changes need to be made and/or communicated.",
                emoji = True
            )
        ]

        if int(summary['parentsrequired']) > int(summary['parentsattendingcount']):
           message_blocks.append([
                SectionBlock(
                    text = f":red-alert: **Not enough parent helpers have signed up**",
                    emoji = True
                )
           ])

        sendMessage(
            "Session plan", 
            channel = "C08C5B8QJE9", 
            blocks = message_blocks
        )
        complete(app.client.files_upload_v2(
            channel="C08C5B8QJE9",
            title=summary['title'],
            content=content,
        ))
        
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e