from config import *
from views import blocks
from osm_admin import *
from utils import slash_request, slash_usage
logging.basicConfig(level=logging.INFO)


###########################################################
### Start the app
###########################################################
if __name__ == "__main__":
    
    app.start(port=int(PORT))
