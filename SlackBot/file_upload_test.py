import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

@app.event("message")
def on_message(event, say, logger):
    print("Message event received!")
    print("Full event payload:", event)

    files = event.get("files", [])
    if files:
        say("I see a file upload! Thanks for sharing 📁")
        logger.info(f"Files detected: {files}")
    else:
        print("No files attached to this message.")

if __name__ == "__main__":
    print("Starting minimal Slack bot for file upload test...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
