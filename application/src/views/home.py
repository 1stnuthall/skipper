from config import *
from resources import OPS_REQUESTS, GROUPS

###########################################################
### Home Screen for the App
# This is the "App Home" screen and presents the user with a list of all
# request types that are currently supported with a button to launch the 
# required request
###########################################################
@app.event("app_home_opened")
def update_home_tab(client, event, logger):

    try:
        ### Set the Default Group Block for the Home Page Display
        group_block = [
            HeaderBlock(
                text=HOME_PAGE_TITLE
            )
        ]
        group_block.append(SectionBlock(
                text=PlainTextObject(text=HOME_PAGE_DESCRIPTION)
            )
        )
        group_block.append(DividerBlock())
        print(group_block)
        ### Add in the Grouped Items
        for group in GROUPS:
            tmp_group_block = [ HeaderBlock(text=group + " Requests:") ]
            for request_name in OPS_REQUESTS:
                if OPS_REQUESTS[request_name]["group"] == group and OPS_REQUESTS[request_name]["enabled"] == "true":
                    tmp_group_block.append(
                        SectionBlock(
                            text=MarkdownTextObject(text=OPS_REQUESTS[request_name]["title_home"]),
                            accessory=ButtonElement(text=PlainTextObject(text="Request"), action_id="req_start", value=request_name)               
                        )
                    )
            if len(tmp_group_block) > 1:
                group_block.extend(tmp_group_block)

        # Add the App Version number
        group_block.append(DividerBlock())
        group_block.append(
            ContextBlock(
                elements = [ 
                    MarkdownTextObject(
                        text="_v{app_version}_".format(
                            app_version = APP_VERSION
                        )
                    ) 
                ]
            )
        )

        print(group_block)

        ### Create the Home View
        client.views_publish(
            user_id=event["user"],
            view=View(
                type="home",
                callback_id="view-id",
                title=PlainTextObject(text=HOME_PAGE_TITLE),
                blocks=group_block,
            )
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

