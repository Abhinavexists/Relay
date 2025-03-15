import logging
from .config import settings
from .setup import setup_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def run_bot() -> None:
    """Run the bot."""
    application = setup_bot()
    
    # Start the Bot
    application.run_polling()
    
    logger.info("Bot started!")

if __name__ == "__main__":
    run_bot()