from config import *

## The "Visit Release" button was clicked, just acknowledge it
@app.action("visit_release")
def visit_button_clicked(ack, body, logger):
    ack()