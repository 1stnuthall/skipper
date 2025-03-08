from . import formUpdate

from config import *
from views import BLK_AZURE_PROJECT_NAME

###########################################################
### Modal Action - add/remove extra Input fields if Service Connection required
###########################################################
@app.action("create_service_connection")
def subscriptionServiceConnection(ack, body, client, logger):
    if len(body['actions'][0]['selected_options']) == 1:
        add_blocks = True
    else:
        add_blocks = False

    formUpdate(
        client = client, 
        body = body,
        additional_blocks = BLK_AZURE_PROJECT_NAME,
        add_blocks = add_blocks
    )
    ack()