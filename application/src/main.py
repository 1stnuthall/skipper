from config import *


# from utils import action_subscription, action_service_connection, action_visit_release
from views import blocks
#from resources import *
from osm_admin import *
from utils import slash_request, slash_usage
logging.basicConfig(level=logging.INFO)


###########################################################
### Start the app
###########################################################
if __name__ == "__main__":
    
    app.start(port=int(PORT))
