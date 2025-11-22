# telegram_bot/handlers/command_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.api_client import get_user_workflows, generate_workflow, register_user, login_user
from ..constants import WORKFLOW_TYPES
from ..config import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    telegram_id = str(user.id)
    
    # Auto-register user with Telegram ID
    try:
        email = f"telegram_{telegram_id}@relay.bot"
        password = f"tg_{telegram_id}_pass"
        full_name = user.full_name or user.first_name or "Telegram User"
        
        await register_user(telegram_id, email, password, full_name)
        await login_user(telegram_id, email, password)
        
        await update.message.reply_text(
            f"👋 Hello {user.first_name}! Welcome to the Relay Workflow Automation Bot.\n\n"
            "You've been automatically registered and logged in!\n\n"
            "Use /help to see available commands."
        )
    except Exception as e:
        # User might already exist, try to login
        try:
            email = f"telegram_{telegram_id}@relay.bot"
            password = f"tg_{telegram_id}_pass"
            await login_user(telegram_id, email, password)
            
            await update.message.reply_text(
                f"👋 Welcome back {user.first_name}!\n\n"
                "Use /help to see available commands."
            )
        except Exception as login_error:
            logger.error(f"Error in start command: {login_error}")
            await update.message.reply_text(
                "❌ Sorry, there was an error setting up your account.\n"
                "Please try again later."
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "🤖 Available Commands:\n\n"
        "/start - Start the bot and register\n"
        "/help - Show this help message\n"
        "/workflows - List your workflows\n"
        "/create - Create a new workflow\n\n"
        "💡 Tip: You can also just describe what you want to automate, "
        "and I'll create a workflow for you!"
    )
    await update.message.reply_text(help_text)

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /login command."""
    await update.message.reply_text(
        "🔑 You're automatically logged in when you use /start!\n"
        "No manual login required."
    )

async def list_workflows_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /workflows command."""
    try:
        telegram_id = str(update.effective_user.id)
        workflows = await get_user_workflows(telegram_id)
        
        if not workflows:
            await update.message.reply_text("📝 You don't have any workflows yet.\nUse /create or just describe what you want to automate!")
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
    except ValueError as e:
        await update.message.reply_text(
            "🔑 Please use /start first to register and login!"
        )
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        await update.message.reply_text(
            "❌ Sorry, there was an error fetching your workflows.\n"
            "Please try again later."
        )

async def create_workflow_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /create command."""
    await update.message.reply_text(
        "🛠️ Just describe what you want to automate!\n\n"
        "For example:\n"
        "• 'Send me an email when a new user signs up'\n"
        "• 'Post to Slack when a payment is received'\n"
        "• 'Summarize documents and save to Drive'\n\n"
        "I'll create the workflow for you!"
    )