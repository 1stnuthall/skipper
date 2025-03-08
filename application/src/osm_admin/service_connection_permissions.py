from views import *

###########################################################
# Request permissions for Service Connection
###########################################################
req_connection_perms = dict(
    group = "Permission",
    title_popup = "Service Connection Perms",
    title_home = ":perms: Request Permissions for a Service Connection",
    devops_pipeline_id = 0,
    command = "service permissions",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SUBSCRIPTION + [
        BLK_PROJECT_NAME,
        BLK_PROJECT_SHORT_NAME,
        BLK_LOCATIONS,
        BLK_PROJECT_OWNER,
        BLK_PROJECT_TEAM,
        BLK_COST_CODE,
        BLK_SERVICE_CONNECTION_NAME,
        BLK_RESOURCE_LIST,
        BLK_PERMISSION_LEVEL
    ]
)