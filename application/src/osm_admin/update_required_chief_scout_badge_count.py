'''
#######################################
Update Required Chief Scout Badge Count

Inputs:
   * OSM Object

Description:
   Counts the number of Activity and Staged badges the Scout has earned.
   If the total is greater than or equal to the requirement for the Chief Scout Award
   then update the Chief Scout badge record.
#######################################
'''

from tabulate import tabulate

from .config import *

from datetime import date

from utils import sendMessage
from views import *
from config import *
from slack_bolt import App, Say, Fail, Complete

from .osm import OSM

def update_required_chief_scout_badge_count(section, user):
    Section = OSM(section)
    logging.info(f"csb={Section.chief_scout_badge}")
    logging.info(f"name={Section.name}")
    logging.info(f"id={Section.id}")
    logging.info(f"term={Section.current_term}")
    badges_required = SECTIONS[Section.name]
    badge_count = []

    badge_flexi = Section.get_badges_flexi(BADGE_FLEXI_NAME)
    badge_records = Section.get_badge_records_by_member()['data']
    chief_scout_badge_record = Section.get_badge_record(badge_id=Section.chief_scout_badge['badge_id'], badge_version=Section.chief_scout_badge['badge_version'])['items']

    for scout_data in Section.scouts:
        scout_info = Section.scouts[scout_data]
        if 'badges' in scout_info:
            activity_count = 0
            staged_count   = 0
            badge_tally = [scout_info['full_name']]
            for badge in scout_info['badges']:
                if badge['completed'] != '0':
                    if badge['badge_group'] == '2':
                        activity_count += 1
                    elif badge['badge_group'] == '3':
                        staged_count += 1
        
            # Update Badge Flexi-Record for Activity Badges
            badge_tally.append(activity_count)
            badge_tally.append(staged_count)

            # Update Badge Flexi Record
            for record in badge_records:
                if record['scoutid'] == scout_data:
                    if record[badge_flexi['activity_badges']] != activity_count:
                        Section.update_flexi_record(badge_flexi['extraid'], scout_data, badge_flexi['activity_badges'], str(activity_count))
                    if record[badge_flexi['staged_badges']] != staged_count:
                        Section.update_flexi_record(badge_flexi['extraid'], scout_data, badge_flexi['staged_badges'], str(staged_count))

            # Update the Chief Scouts Minimum Badge Criteria (if met)
            if (staged_count + activity_count) >= badges_required:
                badge_tally.append("Yes")

                # Create Badge Update Data
                data = {
                    'badge_id': Section.chief_scout_badge['badge_id'],
                    'badge_version': Section.chief_scout_badge['badge_version'],
                    #'field': "_114257",
                    'scoutid': scout_data,
                    'section_id': Section.id,
                    'term': Section.current_term,
                    'value': '[YES]'
                }
                for record in chief_scout_badge_record:
                    if record['scoutid'] == scout_data:
                        #if (data['field'] not in record) or (record[data['field']] != data['value']):
                        print(scout_info['full_name'],"has satisfied badge requirements, updating...")
                        Section.update_badge_record(data)
            
            badge_count.append(badge_tally)

    # Generate Message Block
    message_block = [
        HeaderBlock(
            text = f":{Section.name}: Chief Scout Badge Completion",   
            emoji = True
        ),
        SectionBlock(
            text = f"The Staged and Activity badges earned by each Scout have been tallied!",
            emoji = True
        ),
        DividerBlock(),
        SectionBlock(
            fields = [
                MarkdownTextObject(
                    text = "*Scout Name*"
                ),
                MarkdownTextObject(
                    text = "*Completed*"
                ),
            ]
        )        
    ]

    # Update with Information
    for item in badge_count:
        if len(item) == 4:
            completed = ":white_check_mark:"
        else:
            completed = ":x:"

        message_block.append(
            SectionBlock(
                fields = [
                    MarkdownTextObject(
                        text = item[0]
                    ),
                    MarkdownTextObject(
                        text = completed
                    )
                ]
            )     
        )

    # Send the message to the channel associated with the section requested
    sendMessage(
        channel = Section.name,
        blocks = message_block,
        text = "Chief Scout Tally Complete"
    )

###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_update_chief_scout = dict(
    group = "Section",
    title_popup = "Tally Chief Scout",
    title_home = "Tally Chief Scout",
    action_id = "req_update_chief_scout",
    command = "tally chief scout",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
    ]
)

OPS_REQUESTS.update(req_update_chief_scout=req_update_chief_scout)

@app.action("req_update_chief_scout")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_update_chief_scout['title_popup'],
        req_blocks = req_update_chief_scout['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_update_chief_scout",
    )

@app.view("req_update_chief_scout")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    user = body['user']['id']
    ack()
    update_required_chief_scout_badge_count(section = section, user = user)
    

# This sample custom step formats an input and outputs it
@app.function("req_update_chief_scout")
def step_callback(inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    logger.info("entered function")
    try:
        section = "beavers"
        user = "U08BS48SBL5"
        update_required_chief_scout_badge_count(section = section, user = user)
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e