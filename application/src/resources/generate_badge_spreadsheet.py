from views import *

###########################################################
# Purge a Key Vault from Deleted Vaults
###########################################################
req_badge_spreadsheet = dict(
    group = "Bages",
    title_popup = "Generate Badge Completion Spreadsheet",
    title_home = "Request a spreadsheet showing the completion status of a badge class ",
    devops_pipeline_id = 0,
    command = "badge sheet",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SECTION + [
        BLK_BADGE_TYPE
    ]
)