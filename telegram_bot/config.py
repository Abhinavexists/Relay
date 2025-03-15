import logging
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "populate_by_name": True,
        "extra": "allow",  # Allow extra fields
        "env_file_encoding": "utf-8"
    }

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "workflow_automation"
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    DEBUG: bool = True
    
    # Auth Configuration
    GEMINI_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Import handlers after settings to avoid circular imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from .handlers import command_handlers, message_handlers, callback_handlers

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the dispatcher."""
    logger.error(f"Exception while handling an update: {context.error}")

def setup_bot() -> Application:
    """Set up the bot with handlers."""
    
    # Create the Application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", command_handlers.start_command))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    application.add_handler(CommandHandler("login", command_handlers.login_command))
    application.add_handler(CommandHandler("workflows", command_handlers.list_workflows_command))
    application.add_handler(CommandHandler("create", command_handlers.create_workflow_command))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_message))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_workflow_selection, pattern=r"^workflow_"))
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_workflow_action, pattern=r"^action_"))
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_workflow_execution, pattern=r"^execute_"))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    return application

def run_bot() -> None:
    """Run the bot."""
    application = setup_bot()
    
    # Start the Bot
    application.run_polling()
    
    logger.info("Bot started!")

if __name__ == "__main__":
    run_bot()