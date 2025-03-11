from datetime import date

from utils import sendMessage
from views import *
from config import *
from slack_bolt import App, Say, Fail, Complete



from .config import *
from .osm import OSM

def list_scouts(section, user):
    scouts=""
    for scout in OSM(section).get_scouts():
        if int(scout['age'].split(' ')[0]) < 14:
            scouts+=f"{scout['full_name']}\n"
    sendMessage(
        channel = user,
        text = scouts
    )


###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_list_scouts = dict(
    group = "Section",
    title_popup = "List Scouts",
    title_home = "List Scouts",
    action_id = "req_list_scouts",
    command = "list scouts",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
    ]
)

OPS_REQUESTS.update(req_list_scouts=req_list_scouts)

@app.action("req_list_scouts")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_list_scouts['title_popup'],
        req_blocks = req_list_scouts['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_list_scouts",
    )

@app.view("req_list_scouts")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    user = body['user']['id']
    ack()
    list_scouts(section = section, user = user)
    

# This sample custom step formats an input and outputs it
@app.function("req_list_scouts")
def step_callback(inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    logger.info("entered function")
    try:
        section = "beavers"
        user = "U08BS48SBL5"
        list_scouts(section = section, user = user)
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e