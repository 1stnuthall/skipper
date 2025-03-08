from .tally_challenge_badge_completion import tally_challenge_badge_completion
from .tally_completed_knots import tally_completed_knots
from .update_required_chief_scout_badge_count import update_required_chief_scout_badge_count
from .generate_spreadsheet import generate_spreadsheet
from .login import headers
from .osm import OSM
from .config import *
from utils import cache

from config import *
from tabulate import tabulate
import os, json

###################################################################
# Create Ops Requests object
###################################################################
OPS_REQUESTS = dict(
    req_hello_world = req_hello_world,
    req_kv_purge = req_kv_purge,
    req_kv_restore = req_kv_restore,
    req_azdo_project = req_azdo_project,
    req_resource_group = req_resource_group,
    req_connection_perms = req_connection_perms,
    req_user_perms = req_user_perms
)

###################################################################
### Calculate Groups
###################################################################
groups = []
for req_type in OPS_REQUESTS.keys():
    groups.append(OPS_REQUESTS[req_type]["group"])

# Create a unique set
GROUPS = set(groups)