from config import *
from utils import formOpen

###########################################################
### Modal View Popup
# This is the main "view" that is presented to the user to complete
# It can be called either by the Home Page buttons or by a /request [Request Type] command in slack
###########################################################
@app.action("req_start")
## Display the popup form, the contents of which are defined by the calling process
def display_request_form(ack, body, client, logger):
    ack()

    ### Create the Modal (popup) view
    formOpen(
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "view-id"
    )
