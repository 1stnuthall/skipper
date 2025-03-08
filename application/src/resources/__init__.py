from .hello_world import req_hello_world
from .keyvault_purge import req_kv_purge


###################################################################
# Create Ops Requests object
###################################################################
OPS_REQUESTS = dict(
    req_hello_world = req_hello_world,
    req_kv_purge = req_kv_purge,
    # req_kv_restore = req_kv_restore,
    # req_azdo_project = req_azdo_project,
    # req_resource_group = req_resource_group,
    # req_connection_perms = req_connection_perms,
    # req_user_perms = req_user_perms
)

###################################################################
### Calculate Groups
###################################################################
groups = []
for req_type in OPS_REQUESTS.keys():
    groups.append(OPS_REQUESTS[req_type]["group"])

# Create a unique set
GROUPS = set(groups)