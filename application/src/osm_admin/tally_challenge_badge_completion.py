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

def tally_challenge_badge_completion(section):
    flexi_record_name = 'Challenge Badge Completion'
    flexi_records = section.get_all_flexi_records()
    flexi_record_id = ''
    flexi_record_fields = dict()

    # Find Flexi Record to store Challenge Badge Completion
    for record in flexi_records:
        if record['name'] == flexi_record_name:
            flexi_record_id = record['extraid']
    
    # Create a Flexi Record to hold Challenge Badge completion if it doesn't exist
    if flexi_record_id == '':
        activities = []
        flexi_record_id = section.create_flexi_record(flexi_record_name)
        for activity, activity_data in section.get_badge_structure_by_type(BADGE_NAME['challenge'])['structure'].items():
            if activity != section.chief_scout_badge['badge_identifier']:
                for criteria in activity_data[1]['rows']:
                    activities.append(f'({section.badges["challenge"][activity]["name"]}) {criteria["name"]}')

        flexi_columns = list(dict.fromkeys(activities))
        for column in flexi_columns:
            section.create_flexi_column(flexi_record_id, column)

    flexi_record_fields = section.get_flexi_record_structure(flexi_record_id)['structure'][1]['rows']
    challenge_badges = section.get_badge_structure_by_type(BADGE_NAME['challenge'])['structure']
    

    for badge_name, badge_data in section.badges['challenge'].items():
        record = section.get_badge_record_by_identifier(badge_data['identifier'], badge_name.lower().replace(" ","_"))['items']
        completion = [['Activity','Status']]
        section.get_flexi_column_config(challenge_flexi_record['extraid'], flexi_record_name)
        for challenge in challenge_badges[badge_data['identifier']][1]['rows']:
            column_name = f"({badge_name}) {challenge['name']}"
            column_id = ''
            for scout in challenge_flexi_record['config']:
                if scout['scoutid'] == {challenge['name']}:
                    column_id = scout['scoutid']
                    break
            if column_id == '':
                column_id = section.create_flexi_column(challenge_flexi_record['extraid'], column_name)
                challenge_flexi_record['config'].append({'id':column_id, 'name':column_name, 'width':'150'}) 
            count = 0
            for activity in record:
                if (challenge['field'] in activity) and (activity[challenge['field']][0] != 'x'):
                    count += 1
                    update_value = '[YES]'
                else:
                    update_value = ''
                for scout in challenge_flexi_record['items']:
                    if (scout['scoutid'] == str(activity['scoutid'])) and (scout[column_id] != update_value):
                        scout[column_id] = update_value
                        section.update_flexi_record(challenge_flexi_record['extraid'], scout['scoutid'],column_id, update_value)
                        break
            completion.append([challenge['name'],f'{count} ({round((count / section.size) * 100 )}%)'])

        print("\n{}\n{}\n".format(badge_name, '=' * len(badge_name)))
        print(tabulate(completion, headers='firstrow'))
        