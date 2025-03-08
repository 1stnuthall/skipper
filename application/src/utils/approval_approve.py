from config import *

from . import getInterventionId
from . import sendMessage

@app.action("approve")
## When the "Approve" button has been pressed
def approve(ack, body, client, logger):
    user = body["user"]["id"]
    action_value = json.loads(body["actions"][0]["value"])
    intervention_id = getInterventionId(action_value["buildId"],action_value["stageId"])

    # Send the approval to the Azure Pipeline
    req = requests.patch(
        url = APPROVAL_URL.format(
            organization = ORGANIZATION, 
            project      = PROJECT,
        ),
        data = json.dumps(
            [
                dict(
                    approvalId = intervention_id,
                    status = 4,
                    comment = "Approved via Slack"
                )
            ]
        ),
        headers = AZDO_HEADER,
    )
    print(req.text)
    if req.status_code == 200:
        
        # Add a comment in the thread to say who rejected it and why
        sendMessage(
            text="Approved by <@{user}>.".format(
                user = user
            ), 
            thread = body["message"]["ts"],
            channel = body["channel"]["id"]
        )
    ack()