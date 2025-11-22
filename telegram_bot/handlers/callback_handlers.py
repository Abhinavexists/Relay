# telegram_bot/handlers/callback_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.api_client import (
    get_workflow,
    execute_workflow,
    delete_workflow,
    get_execution_status
)
from ..constants import WORKFLOW_TYPES
from ..config import logger
import json

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    # View workflow details
    if callback_data.startswith("view_workflow_"):
        workflow_id = callback_data.replace("view_workflow_", "")
        await show_workflow_details(update, context, workflow_id)
    
    # Create new workflow - type selection
    elif callback_data.startswith("new_workflow_"):
        workflow_type = callback_data.replace("new_workflow_", "")
        await start_workflow_creation(update, context, workflow_type)
    
    # Create workflow - confirm creation
    elif callback_data.startswith("confirm_workflow_"):
        workflow_id = callback_data.replace("confirm_workflow_", "")
        await confirm_workflow_creation(update, context, workflow_id)
    
    # Create workflow - modify before creation
    elif callback_data.startswith("modify_workflow_"):
        workflow_id = callback_data.replace("modify_workflow_", "")
        await modify_workflow_before_creation(update, context, workflow_id)
    
    # Cancel workflow creation
    elif callback_data == "cancel_workflow":
        if "creating_workflow" in context.user_data:
            del context.user_data["creating_workflow"]
            del context.user_data["workflow_data"]
            del context.user_data["workflow_step"]
        
        await query.edit_message_text("Workflow creation cancelled.")
    
    # Execute workflow
    elif callback_data.startswith("execute_workflow_"):
        workflow_id = callback_data.replace("execute_workflow_", "")
        await execute_workflow_command(update, context, workflow_id)
    
    # Delete workflow
    elif callback_data.startswith("delete_workflow_"):
        workflow_id = callback_data.replace("delete_workflow_", "")
        await delete_workflow_command(update, context, workflow_id)
    
    # Workflow trigger selection
    elif callback_data.startswith("trigger_"):
        trigger_type = callback_data.replace("trigger_", "")
        await handle_trigger_selection(update, context, trigger_type)
    
    # Generic "create workflow" button
    elif callback_data == "create_workflow":
        # Show workflow type selection
        keyboard = []
        
        for workflow_type, description in WORKFLOW_TYPES.items():
            keyboard.append([
                InlineKeyboardButton(
                    description, 
                    callback_data=f"new_workflow_{workflow_type}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "What type of workflow would you like to create?", 
            reply_markup=reply_markup
        )
    
    # Go back to previous workflow creation step
    elif callback_data == "workflow_back":
        await handle_workflow_back(update, context)
    
    else:
        await query.edit_message_text(f"Unknown callback: {callback_data}")

async def show_workflow_details(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_id: str) -> None:
    """Show detailed information about a specific workflow."""
    query = update.callback_query
    telegram_id = str(update.effective_user.id)
    
    try:
        workflow = await get_workflow(telegram_id, workflow_id)
        
        details_text = (
            f"*{workflow['name']}*\n\n"
            f"*Description:* {workflow.get('description', 'No description')}\n"
            f"*Status:* {workflow.get('status', 'draft')}\n"
            f"*Actions:* {len(workflow.get('actions', []))} steps\n\n"
            f"*Trigger:* {workflow.get('trigger', {}).get('type', 'manual')}\n"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("▶️ Execute", callback_data=f"execute_{workflow_id}"),
                InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_{workflow_id}")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(details_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    except Exception as e:
        logger.error(f"Error fetching workflow details: {str(e)}")
        await query.edit_message_text(
            f"Error retrieving workflow details: {str(e)}"
        )

async def start_workflow_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_type: str) -> None:
    """Start the workflow creation process."""
    query = update.callback_query
    
    # Initialize workflow creation state
    context.user_data["creating_workflow"] = True
    context.user_data["workflow_data"] = {"type": workflow_type}
    context.user_data["workflow_step"] = "name"
    
    await query.edit_message_text(
        f"Let's create a new {workflow_type} workflow. First, what would you like to name it?"
    )

async def confirm_workflow_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_id: str) -> None:
    """Create the workflow based on user's confirmation."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    workflow_data = context.user_data.get("workflow_data", {})
    
    try:
        # If this is a new workflow (not an AI-suggested one)
        if workflow_id == "new":
            result = await create_workflow(user_id, workflow_data)
            new_workflow_id = result.get("id")
            
            await query.edit_message_text(
                f"✅ Workflow '{workflow_data.get('name', 'New Workflow')}' created successfully!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("View Details", callback_data=f"view_workflow_{new_workflow_id}")
                ]])
            )
        else:
            # This is an AI-suggested workflow, just confirm it
            await query.edit_message_text(
                f"✅ Workflow created successfully!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("View Details", callback_data=f"view_workflow_{workflow_id}")
                ]])
            )
        
        # Clear workflow creation state
        if "creating_workflow" in context.user_data:
            del context.user_data["creating_workflow"]
            del context.user_data["workflow_data"]
            del context.user_data["workflow_step"]
    
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        await query.edit_message_text(f"Error creating workflow: {str(e)}")

async def modify_workflow_before_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_id: str) -> None:
    """Allow user to modify workflow before creation."""
    query = update.callback_query
    
    # Set up for modification
    context.user_data["creating_workflow"] = True
    context.user_data["workflow_step"] = "name"
    
    if workflow_id == "new":
        workflow_data = context.user_data.get("workflow_data", {})
    else:
        # Get the workflow details from the API
        try:
            workflow = await get_workflow_details(workflow_id)
            context.user_data["workflow_data"] = workflow
            workflow_data = workflow
        except Exception as e:
            logger.error(f"Error fetching workflow for modification: {str(e)}")
            await query.edit_message_text(f"Error preparing workflow for modification: {str(e)}")
            return
    
    await query.edit_message_text(
        f"Let's modify this workflow. What name would you like to give it?\n\n"
        f"Current name: {workflow_data.get('name', 'New Workflow')}"
    )

async def execute_workflow_command(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_id: str) -> None:
    """Execute a workflow and show the results."""
    query = update.callback_query
    telegram_id = str(update.effective_user.id)
    
    await query.edit_message_text("Executing workflow... ⏳")
    
    try:
        result = await execute_workflow(telegram_id, workflow_id, {})
        
        # Build status message with output
        status_text = f"✅ Workflow executed!\n\n"
        status_text += f"Status: {result.get('status', 'unknown')}\n"
        status_text += f"Execution ID: {result.get('id', 'N/A')}\n\n"
        
        # Show output data if available
        output_data = result.get('output_data', {})
        if output_data and len(output_data) > 0:
            status_text += "📊 *Output:*\n"
            for key, value in output_data.items():
                if key != 'input':  # Skip input echo
                    status_text += f"• {key}: {str(value)[:200]}\n"
        
        # Show logs if available
        logs = result.get('logs', [])
        if logs and len(logs) > 0:
            status_text += "\n📝 *Execution Log:*\n"
            for log in logs[-3:]:  # Show last 3 log entries
                msg = log.get('message', '')
                if msg:
                    status_text += f"• {msg}\n"
        
        await query.edit_message_text(
            status_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("View Workflow", callback_data=f"workflow_{workflow_id}")
            ]])
        )
    
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        await query.edit_message_text(
            f"Error executing workflow: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data=f"workflow_{workflow_id}")
            ]])
        )

async def delete_workflow_command(update: Update, context: ContextTypes.DEFAULT_TYPE, workflow_id: str) -> None:
    """Delete a workflow after confirmation."""
    query = update.callback_query
    telegram_id = str(update.effective_user.id)
    
    # First, ask for confirmation
    keyboard = [
        [
            InlineKeyboardButton("Yes, delete it", callback_data=f"confirm_delete_{workflow_id}"),
            InlineKeyboardButton("No, keep it", callback_data=f"workflow_{workflow_id}")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Are you sure you want to delete this workflow? This action cannot be undone.",
        reply_markup=reply_markup
    )

async def handle_trigger_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, trigger_type: str) -> None:
    """Handle workflow trigger type selection."""
    query = update.callback_query
    workflow_data = context.user_data.get("workflow_data", {})
    
    workflow_data["trigger"] = {"type": trigger_type}
    context.user_data["workflow_data"] = workflow_data
    
    if trigger_type == "schedule":
        context.user_data["workflow_step"] = "schedule"
        await query.edit_message_text(
            "When should this workflow run? Please enter a cron expression or a description like 'every Monday at 9am'."
        )
    elif trigger_type == "webhook":
        # Create a webhook trigger automatically
        workflow_data["trigger"]["endpoint"] = f"/webhook/{workflow_data.get('type')}/{hash(workflow_data.get('name', 'new-workflow'))}"
        context.user_data["workflow_data"] = workflow_data
        
        # Show summary and ask for confirmation
        await show_workflow_summary(update, context)
    elif trigger_type == "manual":
        # No additional configuration needed for manual triggers
        workflow_data["trigger"]["manual"] = True
        context.user_data["workflow_data"] = workflow_data
        
        # Show summary and ask for confirmation
        await show_workflow_summary(update, context)

async def handle_workflow_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle going back to the previous workflow creation step."""
    query = update.callback_query
    current_step = context.user_data.get("workflow_step")
    
    if current_step == "trigger":
        context.user_data["workflow_step"] = "description"
        await query.edit_message_text(
            "Let's go back. Please provide a description for your workflow:"
        )
    elif current_step == "schedule" or current_step == "webhook":
        context.user_data["workflow_step"] = "trigger"
        # Show trigger options again
        await query.edit_message_text(
            "How would you like to trigger this workflow?",
            reply_markup=generate_trigger_options_keyboard()
        )
    else:
        # If we can't determine the previous step, just restart
        context.user_data["workflow_step"] = "name"
        await query.edit_message_text(
            "Let's restart. What would you like to name your workflow?"
        )

async def show_workflow_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show a summary of the workflow before creation."""
    query = update.callback_query
    workflow_data = context.user_data.get("workflow_data", {})
    
    summary_text = (
        f"*Workflow Summary*\n\n"
        f"*Name:* {workflow_data.get('name', 'Unnamed Workflow')}\n"
        f"*Type:* {workflow_data.get('type', 'Unknown')}\n"
        f"*Description:* {workflow_data.get('description', 'No description')}\n\n"
        f"*Trigger:* {workflow_data.get('trigger', {}).get('type', 'Manual')}\n"
    )
    
    # Add trigger-specific details
    trigger = workflow_data.get('trigger', {})
    if trigger.get('type') == 'schedule':
        summary_text += f"*Schedule:* {trigger.get('schedule', 'Not specified')}\n"
    elif trigger.get('type') == 'webhook':
        summary_text += f"*Endpoint:* {trigger.get('endpoint', 'Not generated')}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Create Workflow", callback_data=f"confirm_workflow_new"),
            InlineKeyboardButton("🔙 Go Back", callback_data="workflow_back")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        summary_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

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

async def handle_workflow_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle workflow selection from the list."""
    query = update.callback_query
    await query.answer()
    telegram_id = str(update.effective_user.id)
    
    try:
        workflow_id = query.data.split('_')[1]
        workflow = await get_workflow(telegram_id, workflow_id)
        
        keyboard = [
            [
                InlineKeyboardButton("▶️ Execute", callback_data=f"execute_{workflow_id}"),
                InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_{workflow_id}")
            ],
            [InlineKeyboardButton("🔙 Back to List", callback_data="back_to_list")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📋 Workflow Details:\n\n"
            f"Name: {workflow['name']}\n"
            f"Description: {workflow.get('description', 'No description')}\n"
            f"Status: {workflow.get('status', 'Not executed')}\n\n"
            f"Select an action:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error handling workflow selection: {e}")
        await query.edit_message_text(
            "❌ Sorry, there was an error fetching the workflow details.\n"
            "Please try again later."
        )

async def handle_workflow_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle workflow actions (execute/delete)."""
    query = update.callback_query
    await query.answer()
    telegram_id = str(update.effective_user.id)
    
    try:
        action, workflow_id = query.data.split('_')
        
        if action == "execute":
            result = await execute_workflow(telegram_id, workflow_id, {})
            
            # Build output message
            msg = f"✅ Workflow executed!\n\nStatus: {result.get('status', 'unknown')}\n"
            
            # Show output data
            output_data = result.get('output_data', {})
            if output_data:
                msg += "\n📊 Output:\n"
                for key, value in output_data.items():
                    if key != 'input':
                        msg += f"• {key}: {str(value)[:150]}\n"
            
            await query.edit_message_text(msg)
        elif action == "delete":
            await delete_workflow(telegram_id, workflow_id)
            await query.edit_message_text(
                "🗑️ Workflow deleted successfully!\n"
                "Use /workflows to see your remaining workflows."
            )
    except Exception as e:
        logger.error(f"Error handling workflow action: {e}")
        await query.edit_message_text(
            "❌ Sorry, there was an error performing the action.\n"
            "Please try again later."
        )

async def handle_workflow_execution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle workflow execution."""
    query = update.callback_query
    await query.answer()
    telegram_id = str(update.effective_user.id)
    
    try:
        workflow_id = query.data.split('_')[1]
        result = await execute_workflow(telegram_id, workflow_id, {})
        
        # Build output message
        msg = f"✅ Workflow executed!\n\nStatus: {result.get('status', 'unknown')}\n"
        
        # Show output data
        output_data = result.get('output_data', {})
        if output_data:
            msg += "\n📊 Output:\n"
            for key, value in output_data.items():
                if key != 'input':
                    msg += f"• {key}: {str(value)[:150]}\n"
        
        await query.edit_message_text(msg)
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        await query.edit_message_text(
            "❌ Sorry, there was an error executing the workflow.\n"
            "Please try again later."
        )