from config import *

###########################################################
### Handle the /oncall Command
# A user can type "/oncall" anywhere in Slack to find out
# who is on call 
# Using "/oncall" with a date will respond with who will be
# on call on a specific date
###########################################################
@app.command("/oncall")
def handle_command(body, ack, respond, client, logger):
### Handle the /oncall [Date] shortcut

    on_call_date = ""
    date_output  = "today"

    # If a date is passed to the command, use that
    match = re.match("^(\d{1,2})\/(\d{1,2})\/(\d{2,4})$", body["text"])
    if not match is None:
        on_call_date = "&date={}-{}-{}T08:01:00z".format(match.group(3), match.group(2), match.group(1))

        # Create an alternative output to show the specified date was used
        date_output = "on {}".format(date(int(match.group(3)), int(match.group(2)), int(match.group(1))).strftime("%A %B %d %Y"))

    # Get the on call engineer from OpsGenie
    on_call_data = requests.get(OPSGENIE_URL + on_call_date, headers = OPSGENIE_HEADER )
    on_call_user = re.match("([a-z]+)\.([a-z]+).*", json.loads(on_call_data.text)["data"]["onCallParticipants"][0]["name"])

    # Make the name more readable
    engineer = "{} {}".format(on_call_user.group(1), on_call_user.group(2)).title()

    ack(
        # Send the output to the user
        "{} is on call {}".format(engineer, date_output)
    )
