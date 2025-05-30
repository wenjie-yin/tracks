from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TrackBot:
    """Main class for running the tracks service as a Telegram bot."""

    token: str  # Telegram bot token

    def __init__(self, token: str):
        """Initialize the bot with the provided token."""
        self.token = token

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a welcome message when the command /start is issued."""
        await update.message.reply_text(
            "Hi! I'm an echo bot. Send me any message and I'll repeat it back to you!"
        )

    async def echo_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Echo the user message."""

        await update.message.reply_text(update.message.text)

    async def error_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle errors."""

        logger.error(
            "Update caused error. Error: %s. User message (if any): %s",
            context.error,
            update.message.text if update and update.message else None,
        )

    def start(self) -> None:
        """Start the bot."""
        # Create the Application
        application = Application.builder().token(self.token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_command)
        )

        # Add error handler
        application.add_error_handler(self.error_handler)

        # Start the bot
        application.run_polling()


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Please set the TELEGRAM_BOT_TOKEN environment variable.")

    track_bot = TrackBot(token=token)
    track_bot.start()
