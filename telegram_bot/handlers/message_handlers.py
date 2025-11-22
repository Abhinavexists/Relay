# telegram_bot/handlers/message_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.api_client import generate_workflow
from ..config import logger

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    message = update.message.text
    user = update.effective_user
    telegram_id = str(user.id)
    
    # Log the message
    logger.info(f"Message from {user.first_name}: {message}")
    
    try:
        # Show processing message
        processing_msg = await update.message.reply_text("🤖 Analyzing your request and creating a workflow...")
        
        # Generate workflow from natural language
        workflow = await generate_workflow(telegram_id, message)
        
        # Delete processing message
        await processing_msg.delete()
        
        # Show generated workflow
        workflow_text = (
            f"✅ I've created a workflow for you!\n\n"
            f"📋 *{workflow['name']}*\n"
            f"📝 {workflow['description']}\n\n"
            f"Status: {workflow['status']}\n"
            f"Actions: {len(workflow.get('actions', []))} steps"
        )
        
        # Create action buttons
        keyboard = [
            [
                InlineKeyboardButton("▶️ Execute Now", callback_data=f"execute_{workflow['id']}"),
                InlineKeyboardButton("📊 View Details", callback_data=f"workflow_{workflow['id']}")
            ],
            [InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_{workflow['id']}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_markdown(workflow_text, reply_markup=reply_markup)
        
    except ValueError as e:
        await update.message.reply_text(
            "🔑 Please use /start first to register and login!"
        )
    except Exception as e:
        logger.error(f"Error generating workflow: {e}")
        await update.message.reply_text(
            "❌ Sorry, I couldn't create a workflow from that.\n"
            "Please try describing it differently or use /create for guided creation."
        )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle plain text messages from users."""
    user_id = update.effective_user.id
    message_text = update.message.text
    chat_id = update.effective_chat.id
    
    # Check if this is a response to a specific workflow creation step
    user_data = context.user_data
    if user_data and "creating_workflow" in user_data:
        return await handle_workflow_creation_step(update, context)
    
    # Otherwise, try to understand what the user wants to do with natural language
    try:
        await update.message.reply_text("Analyzing your request... 🤔")
        
        # Send the user's natural language request to the AI service
        analysis_result = await analyze_user_request(user_id, message_text)
        
        if analysis_result.get("workflow_detected"):
            # AI detected a workflow the user wants to create
            workflow_suggestion = analysis_result.get("workflow_suggestion", {})
            
            suggestion_text = (
                f"I understand you want to create a workflow that: \n\n"
                f"📋 *{workflow_suggestion.get('description', 'Automates a process')}*\n\n"
                f"Would you like me to set this up for you?"
            )
            
            await update.message.reply_markdown(
                suggestion_text,
                reply_markup=generate_confirm_workflow_keyboard(workflow_suggestion)
            )
        else:
            # No clear workflow intent detected
            await update.message.reply_text(
                "I'm not sure I understand what workflow you want to create. "
                "Could you please describe it in more detail, or use /create to "
                "start the guided workflow creation process?"
            )
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await update.message.reply_text(
            "I encountered an error while processing your request. "
            "Please try again or use /help to see available commands."
        )

async def handle_workflow_creation_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user responses during the workflow creation process."""
    user_data = context.user_data
    current_step = user_data.get("workflow_step")
    workflow_data = user_data.get("workflow_data", {})
    
    message_text = update.message.text
    
    if current_step == "name":
        workflow_data["name"] = message_text
        user_data["workflow_data"] = workflow_data
        user_data["workflow_step"] = "description"
        
        await update.message.reply_text(
            "Great! Now please provide a description for your workflow:"
        )
        
    elif current_step == "description":
        workflow_data["description"] = message_text
        user_data["workflow_data"] = workflow_data
        user_data["workflow_step"] = "trigger"
        
        # Show trigger options
        await update.message.reply_text(
            "How would you like to trigger this workflow?",
            reply_markup=generate_trigger_options_keyboard()
        )
        
    else:
        await update.message.reply_text(
            "I'm not sure what to do with that information in the current workflow creation step. "
            "Please follow the prompts or use /cancel to abort workflow creation."
        )

def generate_confirm_workflow_keyboard(workflow_suggestion):
    """Generate keyboard for workflow confirmation."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, create it", callback_data=f"confirm_workflow_{workflow_suggestion.get('id', 'new')}"),
            InlineKeyboardButton("🔄 Modify first", callback_data=f"modify_workflow_{workflow_suggestion.get('id', 'new')}")
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_workflow")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def generate_trigger_options_keyboard():
    """Generate keyboard for workflow trigger options."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("⏰ Schedule", callback_data="trigger_schedule")],
        [InlineKeyboardButton("🔄 Webhook", callback_data="trigger_webhook")],
        [InlineKeyboardButton("📱 Manual", callback_data="trigger_manual")],
        [InlineKeyboardButton("🔙 Back", callback_data="workflow_back")]
    ]
    
    return InlineKeyboardMarkup(keyboard)