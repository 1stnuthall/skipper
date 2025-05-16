from .tally_challenge_badge_completion import *
#from .tally_completed_knots import tally_completed_knots
from .update_required_chief_scout_badge_count import *
from .generate_spreadsheet import *
from .list_scouts import *
from .send_text_message import *
from .get_programme import *
#from .show_points import *
from .login import headers
from .osm import OSM
from .config import *
from utils import cache, formOpen


from config import *
from tabulate import tabulate
import os, json

###################################################################
### Calculate Groups
###################################################################
groups = []
for req_type in OPS_REQUESTS.keys():
    groups.append(OPS_REQUESTS[req_type]["group"])

# Create a unique set
GROUPS = set(groups)