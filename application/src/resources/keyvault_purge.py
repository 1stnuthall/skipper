from views import *

###########################################################
# Purge a Key Vault from Deleted Vaults
###########################################################
req_kv_purge = dict(
    group = "Key Vault",
    title_popup = "Purge Key Vault",
    title_home = ":kv: Request the _*Purging*_ of a Deleted Azure Key Vault",
    devops_pipeline_id = 0,
    command = "keyvault purge",
    approval_needed = "false",
    enabled = "true",
    blocks = BLK_SUBSCRIPTION + [
        BLK_LOCATIONS,
        BLK_KEY_VAULT
    ]
)