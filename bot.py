import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests
import json

# Basic configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
WORKFLOW_API_URL = "http://localhost:8000/api"  # Your local FastAPI server

# Simple in-memory storage for demo purposes
workflows = {}
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    await update.message.reply_text(
        "👋 Welcome to the Relay - AI Workflow Automator!\n\n"
        "I can help you create automated workflows using natural language.\n\n"
        "Commands:\n"
        "/create - Create a new workflow\n"
        "/list - Show your workflows\n"
        "/help - Get help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "🤖 AI Workflow Automator Help:\n\n"
        "1️⃣ /create - Start creating a workflow with AI\n"
        "2️⃣ /list - View your saved workflows\n"
        "3️⃣ /run [workflow_id] - Run a specific workflow\n"
        "4️⃣ /delete [workflow_id] - Delete a workflow"
    )

async def create_workflow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start workflow creation process."""
    user_id = update.effective_user.id
    user_states[user_id] = "awaiting_description"
    
    await update.message.reply_text(
        "🔮 Let's create a new workflow!\n\n"
        "Describe what you want to automate in simple terms.\n"
        "For example: 'Every day at 9am, check my Gmail for emails with 'invoice' in the subject, "
        "download any PDF attachments, and save them to my Dropbox folder'"
    )

async def list_workflows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all workflows for the user."""
    user_id = update.effective_user.id
    user_workflows = {k: v for k, v in workflows.items() if v.get("user_id") == user_id}
    
    if not user_workflows:
        await update.message.reply_text("You don't have any workflows yet. Use /create to make one.")
        return
    
    message = "🔄 Your workflows:\n\n"
    buttons = []
    
    for workflow_id, workflow in user_workflows.items():
        message += f"ID: {workflow_id} - {workflow['name']}\n"
        buttons.append([
            InlineKeyboardButton(f"Run {workflow_id}", callback_data=f"run_{workflow_id}"),
            InlineKeyboardButton(f"Delete {workflow_id}", callback_data=f"delete_{workflow_id}")
        ])
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages based on their current state."""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    if user_id not in user_states:
        await update.message.reply_text("Use /create to start making a workflow.")
        return
    
    state = user_states[user_id]
    
    if state == "awaiting_description":
        # In a real implementation, this would call your AI workflow generator API
        # For hackathon demo purposes, we'll create a simple mock workflow
        workflow_id = f"wf{len(workflows) + 1}"
        workflow_name = f"Workflow from description: {message_text[:20]}..."
        
        # Mock AI processing
        await update.message.reply_text("🧠 Processing your request...")
        
        try:
            # This would be your actual API call
            # For demo, we'll simulate a successful API response
            """
            response = requests.post(
                f"{WORKFLOW_API_URL}/generate",
                json={"description": message_text}
            )
            workflow_data = response.json()
            """
            
            # Mock workflow data
            workflow_data = {
                "id": workflow_id,
                "name": workflow_name,
                "description": message_text,
                "steps": [
                    {"id": 1, "name": "Parse input", "type": "parser"},
                    {"id": 2, "name": "Process data", "type": "transformer"},
                    {"id": 3, "name": "Generate output", "type": "generator"}
                ],
                "user_id": user_id
            }
            
            workflows[workflow_id] = workflow_data
            
            # Present the workflow to the user
            await update.message.reply_text(
                f"✅ I've created a workflow based on your description!\n\n"
                f"Name: {workflow_name}\n"
                f"ID: {workflow_id}\n"
                f"Steps: {len(workflow_data['steps'])}\n\n"
                f"What would you like to do next?",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("Run Now", callback_data=f"run_{workflow_id}"),
                        InlineKeyboardButton("Delete", callback_data=f"delete_{workflow_id}")
                    ],
                    [InlineKeyboardButton("Create Another", callback_data="create_new")]
                ])
            )
            
            # Reset state
            user_states[user_id] = "idle"
            
        except Exception as e:
            await update.message.reply_text(
                f"Sorry, there was an error creating your workflow: {str(e)}"
            )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith("run_"):
        workflow_id = data[4:]
        if workflow_id in workflows:
            workflow = workflows[workflow_id]
            
            # In a real implementation, this would call your workflow execution API
            # For demo, we'll simulate workflow execution
            await query.edit_message_text(f"⚙️ Running workflow {workflow_id}...")
            
            # Simulate some processing time in a real application
            try:
                # Simulate successful execution
                result = {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "results": {
                        "processed_items": 5,
                        "success_rate": "100%",
                        "execution_time": "2.3s"
                    }
                }
                
                await query.message.reply_text(
                    f"✅ Workflow {workflow_id} executed successfully!\n\n"
                    f"Results:\n"
                    f"- Processed items: {result['results']['processed_items']}\n"
                    f"- Success rate: {result['results']['success_rate']}\n"
                    f"- Execution time: {result['results']['execution_time']}"
                )
            except Exception as e:
                await query.message.reply_text(f"❌ Error executing workflow: {str(e)}")
        else:
            await query.message.reply_text(f"Workflow {workflow_id} not found.")
    
    elif data.startswith("delete_"):
        workflow_id = data[7:]
        if workflow_id in workflows:
            del workflows[workflow_id]
            await query.edit_message_text(f"🗑️ Workflow {workflow_id} deleted.")
        else:
            await query.message.reply_text(f"Workflow {workflow_id} not found.")
    
    elif data == "create_new":
        user_states[user_id] = "awaiting_description"
        await query.message.reply_text(
            "🔮 Let's create another workflow! Describe what you want to automate."
        )

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run a workflow by ID."""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Please provide a workflow ID. Usage: /run workflow_id")
        return
    
    workflow_id = context.args[0]
    if workflow_id in workflows:
        # Simulate workflow execution
        await update.message.reply_text(f"⚙️ Running workflow {workflow_id}...")
        
        # In a real implementation, call your workflow execution API
        result = {
            "status": "success",
            "workflow_id": workflow_id,
            "results": {
                "processed_items": 5,
                "success_rate": "100%",
                "execution_time": "2.3s"
            }
        }
        
        await update.message.reply_text(
            f"✅ Workflow {workflow_id} executed successfully!\n\n"
            f"Results:\n"
            f"- Processed items: {result['results']['processed_items']}\n"
            f"- Success rate: {result['results']['success_rate']}\n"
            f"- Execution time: {result['results']['execution_time']}"
        )
    else:
        await update.message.reply_text(f"Workflow {workflow_id} not found.")

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete a workflow by ID."""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Please provide a workflow ID. Usage: /delete workflow_id")
        return
    
    workflow_id = context.args[0]
    if workflow_id in workflows:
        user_id = update.effective_user.id
        if workflows[workflow_id].get("user_id") == user_id:
            del workflows[workflow_id]
            await update.message.reply_text(f"🗑️ Workflow {workflow_id} deleted.")
        else:
            await update.message.reply_text("You can only delete your own workflows.")
    else:
        await update.message.reply_text(f"Workflow {workflow_id} not found.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("create", create_workflow))
    application.add_handler(CommandHandler("list", list_workflows))
    application.add_handler(CommandHandler("run", run_command))
    application.add_handler(CommandHandler("delete", delete_command))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Button handlers
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()