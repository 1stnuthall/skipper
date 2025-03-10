from config import *

from osm_admin import *
# from utils import action_subscription, action_service_connection, action_visit_release
from views import home, blocks
from resources import *

logging.basicConfig(level=logging.DEBUG)


###########################################################
### Start the app
###########################################################
if __name__ == "__main__":
    
    app.start(port=int(PORT))
