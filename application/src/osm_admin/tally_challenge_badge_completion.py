'''
#######################################
Tally Challenge Badge Completions

Inputs:
   * OSM Object

Description:
   Processes the completion state of the Challenge Badges in the section.
   Outputs data as table in console, as well as a new Flexi Record called 'Challenge Badges'
   which is created if it doesn't exist.
   For completion status of multiple requirements (such as Adventurous Activity) will
   calculate the least number completed assuming requirements are completed in OSM left-to-right
   (which is OSM default).
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

def tally_challenge_badge_completion(body):
    user = body["user_id"]
    if body["channel_name"] == "development":
        print("setting to beavers")
        section_name = "beavers"
    else:
        print(f"section {body['channel_name']}")
        section_name = body["channel_name"]
    Section = OSM(section_name)
    flexi_record_name = 'Challenge Badge Completion'
    flexi_records = Section.get_all_flexi_records()
    flexi_record_id = ''
    flexi_record_fields = dict()

    # Find Flexi Record to store Challenge Badge Completion
    for record in flexi_records:
        if record['name'] == flexi_record_name:
            flexi_record_id = record['extraid']
    
    # Create a Flexi Record to hold Challenge Badge completion if it doesn't exist
    if flexi_record_id == '':
        activities = []
        flexi_record_id = Section.create_flexi_record(flexi_record_name)
        for activity, activity_data in Section.get_badge_structure_by_type(BADGE_NAME['challenge'])['structure'].items():
            if activity != Section.chief_scout_badge['badge_identifier']:
                for criteria in activity_data[1]['rows']:
                    activities.append(f'({Section.badges["challenge"][activity]["name"]}) {criteria["name"]}')

        flexi_columns = list(dict.fromkeys(activities))
        for column in flexi_columns:
            Section.create_flexi_column(flexi_record_id, column)

    flexi_record_fields = Section.get_flexi_record_structure(flexi_record_id)['structure'][1]['rows']
    challenge_badges = Section.get_badge_structure_by_type(BADGE_NAME['challenge'])['structure']
    

    for badge_name, badge_data in Section.badges['challenge'].items():
        record = Section.get_badge_record_by_identifier(badge_data['id'], badge_data['version'], badge_name.lower().replace(" ","_"))['items']
        completion = [['Activity','Status']]
        Section.get_flexi_column_config(flexi_record_id, flexi_record_name)
        for challenge in challenge_badges[badge_data['identifier']][1]['rows']:
            column_name = f"({badge_name}) {challenge['name']}"
            column_id = ''
            for scout in flexi_record_fields['config']:
                if scout['scoutid'] == {challenge['name']}:
                    column_id = scout['scoutid']
                    break
            if column_id == '':
                column_id = Section.create_flexi_column(flexi_record_fields['extraid'], column_name)
                flexi_record_fields['config'].append({'id':column_id, 'name':column_name, 'width':'150'}) 
            count = 0
            for activity in record:
                if (challenge['field'] in activity) and (activity[challenge['field']][0] != 'x'):
                    count += 1
                    update_value = '[YES]'
                else:
                    update_value = ''
                for scout in flexi_record_fields['items']:
                    if (scout['scoutid'] == str(activity['scoutid'])) and (scout[column_id] != update_value):
                        scout[column_id] = update_value
                        Section.update_flexi_record(flexi_record_fields['extraid'], scout['scoutid'],column_id, update_value)
                        break
            completion.append([challenge['name'],f'{count} ({round((count / Section.size) * 100 )}%)'])

        print("\n{}\n{}\n".format(badge_name, '=' * len(badge_name)))
        print(tabulate(completion, headers='firstrow'))

    # Send the message to the channel associated with the section requested
    sendMessage(
        channel = user,
        text = "Challenge Badge Tally Complete"
    )
        
###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_update_challenge_badges = dict(
    group = "Section",
    title_popup = "Update Challenge Badges",
    title_home = "Update Challenge Badges",
    action_id = "req_update_challenge_badges",
    command = "tally challenge badges",
    action = "tally_challenge_badge_completion",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
    ]
)

OPS_REQUESTS.update(req_update_challenge_badges=req_update_challenge_badges)

@app.action("req_update_challenge_badges")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_update_challenge_badges['title_popup'],
        req_blocks = req_update_challenge_badges['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_update_challenge_badges",
    )

@app.view("req_update_challenge_badges")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = body['view']['state']['values']['section']['section']['selected_option']['value']
    user = body['user']['id']
    ack()
    tally_challenge_badge_completion(section = section, user = user)
    

# This sample custom step formats an input and outputs it
@app.function("req_update_challenge_badges")
def step_callback(inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    logger.info("entered function")
    try:
        section = "beavers"
        user = "U08BS48SBL5"
        tally_challenge_badge_completion(section = section, user = user)
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e