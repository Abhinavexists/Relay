# telegram_bot/handlers/command_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.api_client import get_user_workflows, create_workflow
from ..constants import WORKFLOW_TYPES
from ..config import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}! Welcome to the Workflow Automation Bot.\n\n"
        "Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "🤖 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/workflows - List your workflows\n"
        "/create - Create a new workflow\n"
        "/login - Login to your account"
    )
    await update.message.reply_text(help_text)

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /login command."""
    # TODO: Implement login flow
    await update.message.reply_text(
        "🔑 Login functionality coming soon!\n"
        "For now, you can use the bot without login."
    )

async def list_workflows_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /workflows command."""
    try:
        user_id = str(update.effective_user.id)
        workflows = await get_user_workflows(user_id)
        
        if not workflows:
            await update.message.reply_text("📝 You don't have any workflows yet.\nUse /create to create one!")
            return
        
        keyboard = []
        for workflow in workflows:
            keyboard.append([
                InlineKeyboardButton(
                    f"📋 {workflow['name']}",
                    callback_data=f"workflow_{workflow['id']}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📋 Your Workflows:\nSelect a workflow to view details or execute:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        await update.message.reply_text(
            "❌ Sorry, there was an error fetching your workflows.\n"
            "Please try again later."
        )

async def create_workflow_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /create command."""
    # TODO: Implement workflow creation flow
    await update.message.reply_text(
        "🛠️ Workflow creation coming soon!\n"
        "This will allow you to create automated workflows through a simple conversation."
    )