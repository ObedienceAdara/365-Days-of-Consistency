import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)



async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = update.message.document.get_file()
    file.download('temp_document')
    # Process the file here (e.g., extract text)
    await update.message.reply_text("Document received and processed!")
    

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Send me a document, and I'll summarize it for you.")

# Summarize command
async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document_text = update.message.text
    try:
        # Prepare document for summarization
        parser = PlaintextParser.from_string(document_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Summarize to 3 sentences

        # Combine sentences into a single string
        summary_text = ' '.join(str(sentence) for sentence in summary)
        await update.message.reply_text(summary_text)
    except Exception as e:
        logger.error(f"Error summarizing document: {e}")
        await update.message.reply_text("Sorry, I couldn't summarize the document.")

# Main function to handle bot
def main() -> None:
    # Create the bot with your token
    application = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_API_KEY").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, summarize_text))
    application.add_handler(MessageHandler(filters.DOCUMENT, handle_document))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()