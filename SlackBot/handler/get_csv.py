import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

# Store the latest CSV content here (in-memory for demo)
latest_csv_content = None

@app.command("/generate-content")
def handle_command(ack, body, say):
    ack()
    user_id = body["user_id"]
    channel_id = body["channel_id"]
    logger.info(f"User {user_id} triggered /generate-content in channel {channel_id}")
    say(f"👋 Hi <@{user_id}>, please upload your CSV file in this channel.")

@app.event("message")
def handle_file_upload(event, say):
    global latest_csv_content

    files = event.get("files", [])
    if not files:
        return  # no files, ignore

    file_info = files[0]
    if file_info.get("filetype") != "csv":
        say("Please upload a CSV file.")
        return

    file_url = file_info.get("url_private_download")
    if not file_url:
        say("Could not get the file URL.")
        return

    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    response = requests.get(file_url, headers=headers)

    if response.status_code != 200:
        say("Failed to download the CSV file.")
        logger.error(f"Failed to download CSV, status code {response.status_code}")
        return

    latest_csv_content = response.text
    logger.info(f"CSV content downloaded:\n{latest_csv_content}")

    user_id = event.get("user")
    say(f"Thanks <@{user_id}>! Your CSV file has been received and processed :white_check_mark:")

def get_latest_csv():
    """Helper function to get latest CSV content as string."""
    return latest_csv_content

def parse_csv(csv_string):
    """Optional helper: parse CSV string into list of dicts."""
    import csv
    from io import StringIO
    f = StringIO(csv_string)
    reader = csv.DictReader(f)
    return list(reader)

if __name__ == "__main__":
    logger.info("⚡️ Starting Slack Bolt app with Socket Mode...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
