from config import *

from osm_admin import OPS_REQUESTS, GROUPS
###########################################################
## Simple function to create a "Usage" message to a user
## if they just enter "/request" without a valid Request Type keyword
###########################################################
def slashUsage(request: None):
    ## Generate the main intro for the usage information

    print(request)
    group_block = []

    group_block.append(
        HeaderBlock(
            text=COMMAND_TITLE
        )
    )

    if request != "":
    ## Unrecognised Value Provided
        message = ":confused: _*Invalid Request Type:* {request}_".format(
            request = request
        )
        group_block.append(
            SectionBlock(
                text = MarkdownTextObject(
                    text = message
                )
            )
        )

    else:
        group_block.append(
            SectionBlock(
                text = PlainTextObject(
                    text = COMMAND_INFO
                )
            )
        )

    group_block.append(
        SectionBlock(
            text = MarkdownTextObject(
                text = COMMAND_USAGE
            )
        )
    )

    ## Generate the commands and their titles to display to the user
    section_block = ""
    for group in GROUPS:
        for request_name in OPS_REQUESTS:
            if OPS_REQUESTS[request_name]["group"] == group and OPS_REQUESTS[request_name]["enabled"] == "true":
                section_block += "- `{}` - {}\n".format( 
                    OPS_REQUESTS[request_name]["command"], 
                    # Remove icons from titles
                    re.sub(r'(?is):.*:[\s]*', '', OPS_REQUESTS[request_name]["title_home"])
                )

    group_block.append(
        SectionBlock(
            text = MarkdownTextObject(
                text = section_block
            )
        )
    )            
    
    ## Return back to the calling function
    return(group_block)