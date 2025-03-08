from views import *
        
###########################################################
# Request permissions for User
###########################################################
req_user_perms = dict(
    group = "Permission",
    title_popup = "User Perms",
    title_home = ":perms: Request Permissions for a User",
    devops_pipeline_id = 0,
    command = "user permissions",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SUBSCRIPTION + [
        BLK_EMAIL_ADDRESS,
        BLK_RESOURCE_GROUP,
        BLK_RESOURCE_LIST,
        BLK_PERMISSION_LEVEL
    ]
)