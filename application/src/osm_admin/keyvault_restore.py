from views import *

###########################################################
# Restore a Key Vault from Deleted Vaults
###########################################################
req_kv_restore = dict(
    group = "Key Vault",
    title_popup = "Restore Key Vault",
    title_home = ":kv: Request the _*Restoration*_ of a Deleted Azure Key Vault",
    devops_pipeline_id = 0,
    command = "keyvault restore",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SUBSCRIPTION + [
        BLK_LOCATIONS,
        BLK_KEY_VAULT
    ]
)