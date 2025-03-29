"""Variables for SlackOps App."""
import os
import re
import logging
import json
import requests

from datetime import date
from dotenv import load_dotenv

from slack_sdk.models.blocks import *
from slack_bolt import *
from slack_sdk.models.views import View



load_dotenv()

app = App(
    token          = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
)

###################################################################
### Get Environment Variables
###################################################################
SLACK_BOT_TOKEN          = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET     = os.environ.get("SLACK_SIGNING_SECRET")
DEVOPS_TOKEN             = os.environ.get("DEVOPS_TOKEN", "")
APP_VERSION              = str(os.environ.get("APP_VERSION","0.0.1a")).replace("v","")
OPSGENIE_API_KEY         = os.environ.get("OPSGENIE_API_KEY", "")
OPSGENIE_SUBSCRIPTION_ID = os.environ.get("OPSGENIE_SUBSCRIPTION_ID", "")
ORGANIZATION_ID          = os.environ.get("ORGANIZATION_ID", "")
ORGANIZATION             = os.environ.get("ORGANIZATION", "")
PROJECT                  = os.environ.get("PROJECT", "")
OPS_CHANNEL              = os.environ.get("OPS_CHANNEL", "")
OPS_PRIVATE_CHANNEL      = os.environ.get("OPS_PRIVATE_CHANNEL", "")
PORT                     = os.environ.get("PORT", 3000)

###################################################################
### Default Values
###################################################################
ENVIRONMENT              = "Development"
HOME_PAGE_TITLE          = ":bot: Operations"
HOME_PAGE_DESCRIPTION    = """
Hi! I'm Skipper, your Scouting friend.
From here, you can point me in the direction of tasks you want me to do for you.
"""

###################################################################
### Preformatted Intervention Response
###################################################################
INTERVENTION_DATA = {
    "status": "rejected",
    "comment": ""
}

###################################################################
### Request URLs
###################################################################
PIPELINE_RUN_URL =  "https://dev.azure.com/{}/{}/_apis/pipelines/{}/runs?api-version=7.0"
VALIDATION_URL = "https://dev.azure.com/{}/_apis/Contribution/HierarchyQuery/project/{}?api-version=7.0-preview"
APPROVAL_URL = "https://dev.azure.com/{organization}/{project}/_apis/pipelines/approvals?api-version=7.0-preview"
OPSGENIE_URL = "https://api.opsgenie.com/v2/schedules/%s/on-calls?scheduleIdentifierType=id" % OPSGENIE_SUBSCRIPTION_ID

###################################################################
### Request Headers
###################################################################
AZDO_HEADER = {
    "Content-Type": "application/json", 
    "Authorization": "Basic {token}".format(
        token = DEVOPS_TOKEN
    )
}
OPSGENIE_HEADER = {
  "Authorization": "GenieKey {token}".format(
        token = OPSGENIE_API_KEY
    )
}

###################################################################
### Slash Command Info
###################################################################
COMMAND_TITLE = "Scouts Admin"  
COMMAND_INFO  = "Let me help you with something."  
COMMAND_USAGE = """
*Usage:* `/osm [Request Type]`

*Request Types:*
"""

###################################################################
### Calculate the running environment
###################################################################
container_regex = "skipper-app-([a-z]+)-uk[s|w]"
if os.environ.get("CONTAINER_APP_NAME"):
    match = re.match(container_regex, os.environ.get("CONTAINER_APP_NAME"))
    if match.group(1) == "prod":
        ENVIRONMENT = "Production"


