from config import *

###########################################################
## Simple function to send a message
###########################################################
def sendMessage(text, thread = None, channel = None):
    say = Say(
        client = app.client,
        channel = OPS_CHANNEL,
    )

    say(
        text=text,
        thread_ts=thread,
        mrkdwn = True,
        channel = channel
    )
