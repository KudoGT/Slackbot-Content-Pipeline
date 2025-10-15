# 🤖 Slackbot Content Pipeline

A simple AI-powered Slack bot that automates content processing, keyword extraction, and PDF report generation.  
It also emails the final report to the user using **Mailgun API** and allows viewing past processed keyword batches using `/history`.

---

## 📘 Project Overview

This project is made to automate the process of reading messages inside Slack, cleaning the text, extracting important keywords, and making a short summary report in PDF format.  
The bot can also send the report directly to the user’s email and show the history of all past processed keyword sets.

It connects multiple tools together:
- **Slack Bolt SDK** for Slack integration  
- **Natural Language Processing (NLP)** for text handling  
- **ReportLab** for PDF report generation  
- **Mailgun API** for sending emails  

---

## 🧠 Key Features

### ✅ 1. Keyword Extraction
The bot cleans and extracts important keywords from user messages or uploaded CSV files.  
It removes stopwords, duplicate words, and irrelevant data using a small text cleaning function.

### 📄 2. PDF Report Generation
All processed data is stored in a well-formatted PDF file.  
The report includes:
- Date and time  
- Extracted keywords  
- Grouped keyword lists  
- Suggested post ideas and outlines  

### ✉️ 3. Email Sending (Mailgun)
The bot sends the generated PDF report directly to your email address using the **Mailgun REST API**.  
The credentials are securely stored in `.env` file.

### 💬 4. Slack Commands
| Command | Description |
|----------|--------------|
| `/generate-content` | Starts the content processing pipeline. |
| `/history` | Displays a list of previously processed keyword batches. |
| Upload CSV | User can upload a CSV file containing keywords to process automatically. |

### 📜 5. History Tracking
Every processed keyword batch is saved temporarily (can later be stored in a database).  
User can run `/history` to check all old keyword batches.

---

## 🗂 Folder Structure

```bash
slackbot-content-pipeline/
│
├── backend/
│   ├── slackbot.py              # Main Slack bot script (core logic and event handlers)
│   ├── outline.py               # Generates outline text for grouped keywords
│   ├── post_idea.py             # Creates post ideas from keyword groups
│   ├── pdf_generate.py          # Creates and formats the final PDF report
│   ├── send_email.py            # Sends the PDF via Mailgun email API
│
├── utils/
│   ├── cleaning.py              # Cleans and preprocesses keywords/text
│   ├── grouping.py                 # Groups keywords into clusters
|   |-- extractor.py             # extract keywords and content  
│
├── reports/
│   └── (Generated PDFs stored here)
│
├── data/
│   └── (Optional CSV files uploaded by users)
│
├── .env                         # Contains Slack tokens and Mailgun credentials
├── requirements.txt              # All Python dependencies
├── README.md                     # Documentation file


⚙️ Installation and Setup
1️⃣ Clone the Repository
bash
Copy code
git clone https://github.com/KudoGT/slackbot-content-pipeline.git
cd slackbot-content-pipeline

2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt

4️⃣ Create .env File
Create a .env file in the root folder and add:

bash
Copy code
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
MAILGUN_API_KEY=key-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
MAILGUN_DOMAIN=sandboxxxxx.mailgun.org
USER_EMAIL=your_email@example.com


5️⃣ Run the Bot
bash
Copy code
python backend/slackbot.py


💡 How It Works
User runs the /generate-content command in Slack.

The bot asks for text input or CSV upload.

The keywords are cleaned and grouped.

Outline and post ideas are generated for each group.

A professional PDF report is created.

The PDF is uploaded to Slack and emailed to the user.

The batch is saved in memory for /history view.

🧩 Tech Stack Used
Category	Tool / Library
Language	Python 3.x
Slack Integration	Slack Bolt SDK
PDF Creation	ReportLab
Email Service	Mailgun REST API
Environment Management	python-dotenv
Utilities	requests, logging, csv
Future Database	SQLite / MySQL (planned)

🚀 Future Improvements
Database Integration (SQLite / MySQL)
Store user history, processed keywords, and email logs in a structured database instead of local files.

Advanced NLP Processing
Replace simple keyword extraction with TF-IDF, Named Entity Recognition (NER), or topic modeling.

Automatic Scheduling
Add cron jobs to generate reports automatically on a daily or weekly basis.

Dashboard for Visualization
Use Flask or Streamlit to show visual insights of keywords and reports in a web interface.

Multi-User Support
Assign each Slack user their own workspace and email configuration.

🧾 Example Usage
Generate content manually
bash
Copy code
/generate-content AI, robotics, automation
Upload CSV file
Upload a CSV file containing keyword list in the Slack chat when prompted.

Check past batches
bash
Copy code
/history


🧑‍💻 Author
Yash Raj (KudoGT)
AI & ML  | Building automation using NLP + Python
📧 Email: yashraj992002@gmail.com
🐙 GitHub: https://github.com/KudoGT

🏁 Conclusion
The Slackbot Content Pipeline is a complete automation project that mixes text processing, report generation, and Slack integration in one place.
It is modular, easy to understand, and can be extended with advanced AI models or databases in the future.
This project shows how Python can be used to create smart tools for productivity inside modern chat applications.