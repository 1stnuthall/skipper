from config import *
from resources import OPS_REQUESTS

from . import validateInput
from . import apiRequest

###########################################################
### Validate and Submit Request
###########################################################
@app.view("Waas")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, body, logger):

    user = body["user"]["id"]
    user_profile = app.client.users_profile_get(user=user)
    request_type = body["view"]["private_metadata"]

    ### Create a collection of variables
    request_object=dict(
        request_type = dict(value = request_type),
        user_id = dict(value = user),
        user_name = dict(value = user_profile.data["profile"]["real_name"]),
        request_title = dict(value = body["view"]["title"]["text"]),
        approval_needed = dict(value = OPS_REQUESTS[request_type]["approval_needed"])
    )
    request_parameters=dict()
    errors = {}
    value = None
    print("NEW REQUEST:\nUser: {}\nRequest Type: {}".format(request_object["user_name"]["value"], request_object["request_title"]["value"]))
    for key in body["view"]["state"]["values"].keys():
        for input_name in body["view"]["state"]["values"][key].keys():

            ## Send the Input Name and Value and validate it matches the organizational requirements for naming etc
            if body["view"]["state"]["values"][key][input_name]["type"] not in ["static_select", "checkboxes"]:
                input_value = body["view"]["state"]["values"][key][input_name]["value"]
                print("Validating text input of {}: {}".format(input_name, input_value))
                value = validateInput(input_name, input_value)
                if value["validated"] == False:
                    print("Validation failed:", value["error"])
                    errors[input_name] = value["error"]
                else:
                    value = input_value

            ## Handle non-text values
            elif body["view"]["state"]["values"][key][input_name]["type"] == "checkboxes":
                if len(body["view"]["state"]["values"][key][key]["selected_options"]) == 1:
                    value = True
                else:
                    value = False

            else: 
                value = body["view"]["state"]["values"][key][key]["selected_option"]["value"]

            ## Add some protection for Production Environments
            if key == "subscription" and value == "production":
                request_object["approval_needed"] = dict(value = "true")

            if key == "subscription" and ENVIRONMENT == "Development":
                value = "development"
                

            ## Add the value to the variables collection
            request_parameters.update({key:value})

    request_object.update(request_parameters = dict(value = json.dumps(request_parameters)))
    print("REQUEST OBJECT:\n",request_object)

    if len(errors) > 0:
        ## If there were errors, notify the user
        ack (
            response_action = "errors",
            errors = errors
        )
    else:       
        response = apiRequest(request_object, request_type)
        if response.status_code != 200:
            print("Failed:", response.status_code)
            print(response.text)
        else:
            ack()
