import os
import logging
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from backend.pdf_generate import generate_pdf
from backend.outline import generate_outline_for_group
from backend.post_idea import generate_post_idea_for_group
from utils.cleaning import clean_keywords
from utils.grouping import group_keywords
from dotenv import load_dotenv
from backend.send_email import send_email




load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

# Track users awaiting CSV upload
pending_csv_users = {}

# Keep simple in-memory history: user_id -> list of batches
user_history = {}

#  CSV parsing helper
def parse_csv(csv_string):
    from io import StringIO
    import csv
    f = StringIO(csv_string)
    reader = csv.reader(f)
    return [row[0].strip() for row in reader if row and row[0].strip()]

# Slash command handler 
@app.command("/generate-content")
def handle_generate_content(ack, body, say):
    ack()
    user_id = body["user_id"]
    channel_id = body["channel_id"]
    text = body.get("text", "").strip()

    if text.lower() == "csv":
        pending_csv_users[user_id] = channel_id
        say(f"👋 Hi <@{user_id}>, please upload your CSV file in this channel.")
        return

    keywords = [kw.strip() for kw in text.replace(",", "\n").split("\n") if kw.strip()]
    if not keywords:
        say("No keywords detected. Please provide some keywords.")
        return

    say(":gear: Generating content ideas, please wait…....")
    send_pipeline_results(say, keywords, user_id, channel_id)

# Handle uploaded CSV files 
@app.event("message")
def handle_file_upload(event, say):
    user_id = event.get("user")
    channel_id = event.get("channel")
    files = event.get("files", [])

    if user_id not in pending_csv_users or channel_id != pending_csv_users[user_id]:
        return

    if not files:
        say(f"<@{user_id}>, no file detected. Please attach a CSV file.")
        return

    file_info = files[0]
    if file_info.get("filetype") != "csv":
        say(f"<@{user_id}>, please upload a CSV file.")
        return

    file_url = file_info.get("url_private_download")
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    response = requests.get(file_url, headers=headers)
    if response.status_code != 200:
        say(f"<@{user_id}>, failed to download the CSV file.")
        logger.error(f"Failed to download CSV, status code {response.status_code}")
        return

    keywords = parse_csv(response.text)
    if not keywords:
        say(f"<@{user_id}>, no keywords found in CSV.")
        return

    del pending_csv_users[user_id]

    say(":gear: Generating content ideas, please wait… :hourglass_flowing_sand:")
    send_pipeline_results(say, keywords, user_id, channel_id)

# Send results for each group with post idea 
def send_pipeline_results(respond_fn, keywords, user_id, channel_id):
    cleaned_keywords = clean_keywords(keywords)
    if not cleaned_keywords:
        respond_fn("No valid keywords after cleaning. Try different keywords.")
        return

    groups = group_keywords(cleaned_keywords)
    if not groups:
        respond_fn("Failed to group keywords. Try with more diverse keywords.")
        return

    results = []
    for i, (group_id, kw_list) in enumerate(groups.items(), 1):
        outline = generate_outline_for_group(kw_list)
        post_idea = generate_post_idea_for_group(kw_list, outline)

        results.append({
            "group": i,
            "keywords": kw_list,
            "outline": outline,
            "post_idea": post_idea
        })


        # Save to user history (last 10 batches)
        user_history.setdefault(user_id, []).append({
            "keywords_raw": keywords,
            "keywords_cleaned": cleaned_keywords,
            "results": results
        })
        if len(user_history[user_id]) > 10:
            user_history[user_id].pop(0)



    # Send message blocks to Slack
    blocks = []
    for item in results:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*Group {item['group']}*\n"
                    f"*Keywords:* {', '.join(item['keywords'])}\n"
                    f"*Post Idea:* {item['post_idea']}\n"
                    f"*Outline:*\n{item['outline']}"
                )
            }
        })
        blocks.append({"type": "divider"})

    respond_fn(blocks=blocks)

    # Generate PDF
    pdf_path = generate_pdf(results)

    
    # Upload PDF to Slack using files.upload_v2 
    try:
        with open(pdf_path, "rb") as f:
            app.client.files_upload_v2(
                channel=channel_id,
                file=f,
                title="Content Generation Report",
                initial_comment=f"<@{user_id}>, your content generation report PDF is ready!"
            )
    except Exception as e:
        logger.error(f"Failed to upload PDF: {e}")
        respond_fn(f"<@{user_id}>, failed to upload PDF. You can check logs.")

    
    # Optional: Send PDF via Mailgun email
    user_email = "example@gmail.com"

    if pdf_path and user_email:
        try:
            email_status = send_email(
                to_email=user_email,
                subject="Your SlackBot Content Report",
                text="Hi! Attached is your content report PDF.",
                pdf_path=pdf_path
            )
            respond_fn(f"📧 {email_status}")
        except Exception as e:
            respond_fn(f"Failed to send PDF via email: {e}")
            logger.error(f"Email sending error: {e}")



# --- Slash command handler for /history ---
@app.command("/history")
def handle_history(ack, body, say):
    ack()
    user_id = body["user_id"]

    if user_id not in user_history or not user_history[user_id]:
        say("ℹNo history found for you.")
        return

    # Show last 5 batches
    history_batches = user_history[user_id][-5:]
    blocks = []
    for idx, batch in enumerate(reversed(history_batches), 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*Batch {idx}*\n"
                    f"Raw Keywords: {', '.join(batch['keywords_raw'])}\n"
                    f"Cleaned Keywords: {', '.join(batch['keywords_cleaned'])}\n"
                    f"Groups: {', '.join([', '.join(g['keywords']) for g in batch['results']])}"
                )
            }
        })
        blocks.append({"type": "divider"})

    say(blocks=blocks)




# --- Run Slackbot ---
if __name__ == "__main__":
    logger.info("Starting Slack Bolt ......")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
