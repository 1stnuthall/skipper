from config import *
from osm_admin import OPS_REQUESTS

###########################################################
## Simple function to simplify the updating of the Request
## popup - rather than having the same code in multiple places
###########################################################
def formUpdate(client, body, additional_blocks, add_blocks, callback_id = "view-id"):
    ### Get the values for the selected request type
    req_id = body["view"]["private_metadata"]
    view_id = body["view"]["id"]
    body_blocks = body['view']['blocks']
    req_title  = OPS_REQUESTS[req_id]['title_popup']

    #additional_blocks = json.loads(additional_blocks)
    block_exists = False
    for extra_block in additional_blocks:
        for block in body_blocks:
            if extra_block['block_id'] == block['block_id']:
                    block_exists = True
                    if not add_blocks:
                        body_blocks.remove(block)

    if add_blocks and not block_exists:
        body_blocks.extend(additional_blocks)

    return(client.views_update(
            view_id = view_id,
            view = View(
                type = "modal",
                private_metadata = req_id,
                callback_id = callback_id,
                title = PlainTextObject(text=req_title),
                submit = PlainTextObject(text="Submit"),
                close = PlainTextObject(text="Cancel"),
                blocks = body_blocks,
            ),
        )
    )



