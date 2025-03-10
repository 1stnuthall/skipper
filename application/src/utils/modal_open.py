from config import *

###########################################################
## Simple function to simplify the creation of the Request
## popup - rather than having the same code in multiple places
###########################################################
def formOpen(client, req_title, req_blocks, trigger_id, view_id, req_id, callback_id):
    return(client.views_open(
            trigger_id = trigger_id,
            view_id = view_id,
            view = View(
                type = "modal",
                private_metadata = req_id,
                callback_id = callback_id,
                title = PlainTextObject(text=req_title),
                submit = PlainTextObject(text="Submit"),
                close = PlainTextObject(text="Cancel"),
                blocks = req_blocks,
            ),
        )
    )