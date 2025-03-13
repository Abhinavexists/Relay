# Workflow Automation System

A powerful workflow automation system that uses AI to create and execute automated workflows through a Telegram bot interface. The system leverages LangChain and OpenAI to understand natural language commands and generate appropriate workflows.

## 🌟 Features

- 🤖 Natural Language Workflow Creation
- 📱 Telegram Bot Interface
- 🔄 Automated Workflow Execution
- 📧 Email Integration
- 📁 File System Operations
- 🌐 Web Scraping Capabilities
- 🔒 Secure Authentication
- 📊 Monitoring and Logging

## 🏗️ Architecture

The system consists of three main components:

1. **Telegram Bot** (`telegram_bot/`)
   - Handles user interactions
   - Processes commands and messages
   - Manages workflow execution requests

2. **Backend API** (`backend/`)
   - FastAPI-based REST API
   - Workflow management
   - User authentication
   - AI service integration

3. **AI Service**
   - LangChain-based workflow generation
   - Natural language processing
   - Tool selection and orchestration

For a detailed architecture diagram and component breakdown, see [architecture.html](architecture.html).

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- MongoDB
- Telegram Bot Token
- OpenAI API Key

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/workflow-automation.git
   cd workflow-automation
   ```

2. Create and configure environment variables:
   ```bash
   cp env-example.txt .env
   ```
   Edit `.env` with your configuration:
   ```bash
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000

   # MongoDB Configuration
   MONGODB_URI=mongodb://mongodb:27017
   MONGODB_DB_NAME=workflow_automation

   # Telegram Bot Configuration
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

   # AI Service Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # JWT Configuration
   SECRET_KEY=your-secret-key-for-jwt

   # Debug Mode
   DEBUG=true
   ```

### Running with Docker

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. The services will be available at:
   - Backend API: http://localhost:8000
   - MongoDB: mongodb://localhost:27017
   - Telegram Bot: Start chatting with your bot on Telegram

### Manual Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the services:
   ```bash
   # Start MongoDB (if not using Docker)
   mongod

   # Start the backend API
   cd backend
   uvicorn main:app --reload

   # Start the Telegram bot
   cd telegram_bot
   python main.py
   ```

## 📱 Telegram Bot Commands

- `/start` - Initialize the bot
- `/help` - Show available commands
- `/workflows` - List your workflows
- `/create` - Create a new workflow
- `/login` - Authenticate with the system

## 🔧 Development

### Project Structure

```
workflow-automation/
├── backend/
│   ├── api/
│   ├── core/
│   ├── models/
│   └── services/
├── telegram_bot/
│   ├── handlers/
│   ├── utils/
│   └── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Adding New Features

1. Create new workflow tools in `backend/core/tools/`
2. Add new API endpoints in `backend/api/`
3. Implement new bot commands in `telegram_bot/handlers/`
4. Update the AI service in `backend/services/ai_service.py`

## 🔒 Security

- JWT-based authentication
- Role-based access control
- Environment variable encryption
- Secure API communication
- Input validation

## 📊 Monitoring

- Application logs
- System metrics
- Error tracking
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [MongoDB](https://www.mongodb.com/)

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
