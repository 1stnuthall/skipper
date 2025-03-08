from views import *

###########################################################
# Request new Azure Resource Group
###########################################################
req_resource_group = dict(
    group = "Resource",
    title_popup = "New Azure Resource Group",
    title_home = ":rg: Request new Azure Resource Group",
    devops_pipeline_id = 0,
    command = "resource group",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SUBSCRIPTION + [
        BLK_PROJECT_NAME,
        BLK_PROJECT_SHORT_NAME,
        BLK_LOCATIONS,
        BLK_PROJECT_OWNER,
        BLK_PROJECT_TEAM,
        BLK_COST_CODE,
        BLK_SERVICE_CONNECTION
    ]
)