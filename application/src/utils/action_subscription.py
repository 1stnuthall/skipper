from . import formUpdate

from config import *
from views import BLK_PRODUCTION

###########################################################
### Modal Action - add/remove extra Input fields if Production
###########################################################
@app.action("subscription")
def subscriptionAction(ack, body, client, logger):
    # Identify if using a protected environment
    if body['actions'][0]['selected_option']['value'] in ["production"]:
        is_prod = True
    else:
        is_prod = False

    formUpdate(
        client = client, 
        body = body,
        additional_blocks = BLK_PRODUCTION,
        add_blocks = is_prod
    )
    ack()