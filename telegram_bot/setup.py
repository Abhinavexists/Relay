from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from .config import settings
from .handlers import command_handlers, message_handlers, callback_handlers

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
    
    return application 