"""Request Form Block Definitions."""
from slack_sdk.models.blocks import *

###########################################################
## Block Types
###########################################################

BLK_SECTION = InputBlock(
    block_id = "section",
    label = "Section",
    element = StaticSelectElement(
       action_id = "section",
       placeholder = "Select section",
       options = [
          Option(label = "Beavers", value = "beavers"),
          Option(label = "Cubs",    value = "cubs"),
          Option(label = "Scouts",  value = "scouts")
       ]
    )
)

BLK_MESSAGE = InputBlock(
  block_id = "message",
  label = TextObject(type="plain_text", text="Message"),
  element = PlainTextInputElement(action_id="message", placeholder="Enter a message to send to all section members")
)

BLK_COST_CODE = InputBlock(
    block_id = "cost_code",
    label = TextObject(type="plain_text", text="Cost Code"),
    element = PlainTextInputElement(action_id="cost_code", placeholder="P012345")
)

BLK_BADGE_TYPE = InputBlock(
    block_id = "badge_type",
    label = "Badge Type",
    element = StaticSelectElement(
       action_id = "badge_type",
       placeholder = "challenge",
       options = [
          Option(label = "Challenge", value = "challenge"),
          Option(label = "Activity",  value = "activity"),
          Option(label = "Staged",    value = "staged")
       ]
    )
)


###################################################################
### Additional blocks to add if Production Environment is selected
###################################################################
BLK_PRODUCTION = [
    dict(
        type = "input",
        block_id = "change_request",
        label = dict(type="plain_text", text="Change or Jira Number"),
        element = dict(type="plain_text_input", action_id="change_request", placeholder=dict(type="plain_text", text="CHG0123456"))
    ),
    dict(
        type = "input",
        block_id = "request_reason",
        label = dict(type="plain_text", text="Reason for the request"),
        element = dict(type="plain_text_input", action_id="request_reason")
    )
]
