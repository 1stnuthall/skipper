from config import *
from . import sendMessage
from . import getInterventionId

@app.action("reject")
## When the "Reject" button is pressed
def reject(ack, body, client, logger):
    ack()

    ## Open a modal view to capture a reason for the rejection
    ## This then passes on to the following @app.view
    forwarding_data = "{}_{}_{}".format(
        body["actions"][0]["value"], 
        body["channel"]["id"],
        body["message"]["ts"]
    )
    print(forwarding_data)
    client.views_open(
        trigger_id = body["trigger_id"],
        view_id = "home",
        view = View(
            type = "modal",
            private_metadata = forwarding_data,
            callback_id = "reject",
            title = PlainTextObject(text="Rejection Reason"),
            submit = PlainTextObject(text="Submit"),
            close = PlainTextObject(text="Cancel"),
            blocks = [
                InputBlock(
                    block_id="reject_reason",
                    element=PlainTextInputElement(
                        action_id="reject_reason",
                    ),
                    label=PlainTextObject(text="Reason for rejection"),
                ),
            ],
        ),
    )

@app.view("reject")
## Use the response from the rejection modal view and submit the rejection to Azure DevOps
def handle_reject(ack, body, respond, logger):

    user = body["user"]["id"]
    action_value = json.loads(body["view"]["private_metadata"].split('_')[0])
    ops_channel = body["view"]["private_metadata"].split('_')[1]
    ops_thread = body["view"]["private_metadata"].split('_')[2]
    intervention_id = getInterventionId(action_value["buildId"],action_value["stageId"])
    reject_reason = body["view"]["state"]["values"]["reject_reason"]["reject_reason"]["value"]
    
    # Send the rejection to the Azure Pipeline
    req=requests.patch(
        url=APPROVAL_URL.format(
            organization = ORGANIZATION, 
            project      = PROJECT,
        ),
        data = json.dumps(
            [
                dict(
                    approvalId = intervention_id,
                    status = 8,
                    comment = reject_reason
                )
            ]
        ),
        headers=AZDO_HEADER,
    )
    print(req.text)
    if req.status_code == 200:
        # Add a comment in the thread to say who rejected it and why
        sendMessage(
            text="Rejected by <@{user}>.\n*Reason:* {reason}".format(
                user = user, 
                reason = reject_reason
            ), 
            thread = ops_thread,
            channel = ops_channel
        )
    ack()