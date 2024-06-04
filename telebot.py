import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from bs4 import BeautifulSoup
import requests
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Fetch "Never have I ever" questions from the website
def fetch_questions():
    url = "https://www.scienceofpeople.com/never-have-i-ever-questions/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    qlist = soup.find_all("li")
    never_have_i_ever_questions = []
    for i in qlist:
        if "Never have I ever" in i.text:
            never_have_i_ever_questions.append(i.text)
    return never_have_i_ever_questions

# List of "Never Have I Ever" questions
questions = fetch_questions()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome to "Never Have I Ever"! Type /next to get a question, or /stop to end the game.')

async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the next "Never Have I Ever" question."""
    question = random.choice(questions)
    await update.message.reply_text(question)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop the bot."""
    await update.message.reply_text('Thanks for playing "Never Have I Ever"! Type /start to play again.')

def main() -> None:
    """Start the bot."""
    # Replace 'YOUR TOKEN HERE' with your actual bot token
    application = Application.builder().token("enter the api of your telegram bot").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("next", next_question))
    application.add_handler(CommandHandler("stop", stop))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
