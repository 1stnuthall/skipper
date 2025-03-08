from config import *

from osm_admin import *
from utils import *
from utils import action_subscription, action_service_connection, action_visit_release
from views import home, blocks, request, modal
from views import request

logging.basicConfig(level=logging.WARNING)


###########################################################
### Start the app
###########################################################
if __name__ == "__main__":
    app.start(port=int(PORT))
