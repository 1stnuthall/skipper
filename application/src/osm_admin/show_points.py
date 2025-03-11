from datetime import date

from utils import sendMessage
from views import *
from config import *


from .config import *
from .osm import OSM

def show_points(section, user):
    points=""
    for patrol in OSM(section).get_patrols():
        points+=f'{patrol['name']}={patrol['points']}\n'
        sendMessage(
            channel = user,
            text = points
        )


###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_show_points = dict(
    group = "Section",
    title_popup = "Show Points",
    title_home = "Show Points",
    action_id = "req_show_points",
    command = "show points",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
    ]
)

OPS_REQUESTS.update(req_show_points=req_show_points)

@app.action("req_show_points")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_show_points['title_popup'],
        req_blocks = req_show_points['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_show_points",
    )

@app.view("req_show_points")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    user = body['user']['id']
    ack()
    show_points(section = section, user = user)
    