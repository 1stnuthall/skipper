from datetime import date

from utils import sendMessage
from views import *
from config import *
from slack_bolt import App, Say, Fail, Complete

from .config import *
from .osm import OSM

def list_scouts(body):
    if body["channel_name"] == "development":
        print("setting to beavers")
        section_name = "beavers"
    else:
        print(f"section {body['channel_name']}")
        section_name = body["channel_name"]
    user = body["user_id"]
    scouts=""
    for scout in OSM(section_name).get_scouts():
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
    action = "list_scouts",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
    ]
)

OPS_REQUESTS.update(req_list_scouts=req_list_scouts)

@app.action("req_list_scouts")
# Actions to perform on Slash Command
def display_request_form(ack, body, client, logger, fail: Fail, complete: Complete):
    ack()
    logger.info("entered function")
    try:
        section = body["channel_id"]
        user = body["user_id"]
        list_scouts(section = section, user = user)
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e

