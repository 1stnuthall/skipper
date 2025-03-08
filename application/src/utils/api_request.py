from osm_admin import OPS_REQUESTS
from config import *

###########################################################
## Simple function to submit an API request to the relevant Release Pipeline,
## triggering a release to be created with the captured variables
###########################################################
def apiRequest(request_object, request_type):    
    headers = AZDO_HEADER
    devops_pipeline_id = OPS_REQUESTS[request_type]["devops_pipeline_id"]
    payload = dict(
        variables = request_object
    )
    response = requests.post(PIPELINE_RUN_URL.format(ORGANIZATION, PROJECT, devops_pipeline_id), json = payload, headers = headers )
    print(response.text)
    return(response)