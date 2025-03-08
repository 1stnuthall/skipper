from views import *

###########################################################
# Request new Azure DevOps Project
###########################################################
req_azdo_project = dict(
    group = "Resource",
    title_popup = "New Azure DevOps Project",
    title_home = ":azdo: Request new Azure DevOps Project",
    devops_pipeline_id = 0,
    command = "project",
    approval_needed = "true",
    enabled = "true",
    blocks = [
        BLK_PROJECT_NAME,
        BLK_PROJECT_SHORT_NAME,
        BLK_PROJECT_OWNER,
        BLK_PROJECT_TEAM,
        BLK_COST_CODE
    ]
)