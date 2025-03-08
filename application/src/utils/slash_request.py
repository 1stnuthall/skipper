from config import *

from utils import formOpen
from osm_admin import OPS_REQUESTS

from .slash_usage import slashUsage

###########################################################
### Handle the /request Command
# A user can type "/request" anywhere in Slack 
# The command is expecting a command keyword (such as project or resourcegroup),
# if the keyword is not submitted, the user will get a "usage" message.
# Otherwise, the relevant modal view is presented
###########################################################
@app.command("/request")
def handle_command(body, ack, respond, client, logger):
### Handle the /request [Request Type] shortcut

    ## Find the Ops Request ID to use
    req_id = None
    for req in OPS_REQUESTS.keys():
        if OPS_REQUESTS[req]["command"] == body["text"]:
            req_id = req

    if req_id == None:
        # No req_id was found
        ack(
            blocks=slashUsage(body["text"]),
        )
    else:
        ack()
        ### Create the Modal (popup) view
        res = formOpen(
            client = client, 
            trigger_id = body["trigger_id"],
            view_id = "home",
            req_id = req_id,
            callback_id = "view-id"
        )
        logging.warning(res)