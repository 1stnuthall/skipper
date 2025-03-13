from datetime import date

from openpyxl import Workbook
from string import ascii_uppercase as col

from utils import sendMessage
from views import *
from config import *


from .config import *
from .osm import OSM

def generate_spreadsheet(badge_type, section, user):
    print(f"Generating {badge_type.title()} Badge Records for {section.name.title()}...")
    xl = Workbook()
    filename = f"{section.group} {section.name.title()} - {badge_type.title()} ({date.today()}).xlsx"
    sheet = xl.active
    badge_structure = section.get_badge_structure_by_type(BADGE_NAME[badge_type])['structure']
    
    for key, value in section.badges[badge_type].items():
        print(f"\nCapturing {key} badge detail...")
        if sheet.title != 'Sheet':
            sheet = xl.create_sheet()
        sheet.title = key.title()
        xlrow = 1
        xlcol = 0
        sheet[f"{col[xlcol]}{xlrow}"] = 'Scout'
        sheet[f"{col[xlcol]}{xlrow}"].font = XL_HEADER
        for scoutid, scout in section.scouts.items():
            if 'badges' in scout:
                xlrow += 1
                sheet[f"{col[xlcol]}{xlrow}"] = f"{scout['full_name']}"
        badge_id = "{0}_{1}".format(value['id'], value['version'])
        
        for row in badge_structure[badge_id][1]['rows']:
            xlcol += 1
            xlrow = 1
            sheet[f"{col[xlcol]}{xlrow}"] = row['name']
            sheet[f"{col[xlcol]}{xlrow}"].font = XL_HEADER
            sheet[f"{col[xlcol]}{xlrow}"].alignment = XL_SLANTED

            xlrow += 1
            badge_completion = section.get_badge_record(value['id'],value['version'])['items']

            for scout in badge_completion:
                if row['field'] in scout.keys():
                    sheet[f"{col[xlcol]}{xlrow}"] = scout[row['field']]
                xlrow += 1
        
    print(f"Creating {filename} file")
    xl.save(f"{filename}")
    # The name of the file you're going to upload
    file_name = filename
    # ID of channel that you want to upload file to

    # Call the files.upload method using the WebClient
    # Uploading files requires the `files:write` scope
    result = app.client.files_upload_v2(
        channel="C08C5B8QJE9",
        initial_comment=f"Here is the latest {badge_type} badge completion status spreadsheet.",
        file=filename,
    )
    # Log the result
    logging.info(result)


###########################################################
# Generate a spreadsheet showing badge completion for a section
###########################################################
req_badge_spreadsheet = dict(
    group = "Bages",
    title_popup = "Generate Spreadsheet",
    title_home = "Generate Badge Spreadsheet",
    action_id = "req_badge_spreadsheet",
    action = "generate_spreadsheet",
    command = "badge status",
    approval_needed = "false",
    enabled = "true",
    blocks = [
        BLK_SECTION,
        BLK_BADGE_TYPE
    ]
)

OPS_REQUESTS.update(req_badge_spreadsheet=req_badge_spreadsheet)

@app.action("req_badge_spreadsheet")
## Display the popup form
def display_request_form(ack, body, client, logger):
    ack()
    ### Create the Modal (popup) view
    formOpen(
        req_title = req_badge_spreadsheet['title_popup'],
        req_blocks = req_badge_spreadsheet['blocks'],
        client = client, 
        trigger_id = body["trigger_id"],
        view_id = "home",
        req_id = body["actions"][0]["value"],
        callback_id = "req_badge_spreadsheet",
    )

@app.view("req_badge_spreadsheet")
## Handle the response from the relevant modal view form completed by the user
def view_submission(ack, say, body, logger):
    section = OSM(body['view']['state']['values']['section']['section']['selected_option']['value'])
    category = body['view']['state']['values']['badge_type']['badge_type']['selected_option']['value']
    user = body['user']['id']
    ack()
    generate_spreadsheet(badge_type = category, section = section, user = user)
    