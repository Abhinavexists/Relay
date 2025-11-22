# Relay - AI-Powered Workflow Automation Platform

Relay is a powerful workflow automation platform that enables users to create, manage, and execute complex workflows through natural language descriptions. Built with FastAPI, MongoDB, and integrated with Google's Gemini AI, Relay makes automation accessible through both a REST API and a Telegram bot interface.

## 🌟 Features

### Core Capabilities
- **Natural Language Workflow Creation**: Describe workflows in plain English, and AI generates the complete workflow structure
- **Real Workflow Execution**: Execute workflows with graph traversal, handling complex dependencies and parallel execution
- **Multiple Action Types**: Support for AI tasks (summarize, extract, classify, generate), HTTP requests, email sending, and data transformation
- **Telegram Bot Integration**: Create and execute workflows directly from Telegram
- **JWT Authentication**: Secure API access with JWT tokens and argon2 password hashing
- **Execution Tracking**: Monitor workflow executions with detailed logs and status updates

### Supported Actions
- **AI Tasks**: Summarization, extraction, classification, and content generation using Gemini AI
- **HTTP Requests**: Make API calls to external services
- **Email**: Send automated emails (simulated, configurable for SMTP)
- **Data Transformation**: Transform and manipulate data within workflows

## 🏗️ Architecture

```
Relay/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   │   └── routes/         # User, workflow, and execution endpoints
│   ├── core/               # Security and configuration
│   ├── database/           # MongoDB connection
│   ├── models/             # Pydantic models
│   └── services/           # Business logic (AI, tools, workflows)
├── telegram_bot/           # Telegram bot integration
│   ├── handlers/           # Command and callback handlers
│   └── utils/              # API client for backend communication
└── verify_backend.py       # Verification script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MongoDB
- Google Gemini API key
- Telegram Bot Token (optional, for Telegram integration)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abhinavexists/Relay.git
cd Relay
```

2. **Set up environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# OR using uv (recommended)
uv pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here  # Optional
JWT_SECRET_KEY=your_secret_key_here
```

4. **Start MongoDB**
```bash
sudo systemctl start mongod
```

5. **Run the backend**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
# OR using uv
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

6. **Run the Telegram bot** (optional)
```bash
python -m telegram_bot.bot
# OR using uv
uv run python -m telegram_bot.bot
```

## 📖 Usage

### REST API

#### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"
```

#### 3. Generate a Workflow from Natural Language
```bash
curl -X POST http://localhost:8000/api/workflows/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Summarize this text: Artificial intelligence is transforming how we work and live."
  }'
```

#### 4. Execute a Workflow
```bash
curl -X POST http://localhost:8000/api/execute/WORKFLOW_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 5. Get Execution Status
```bash
curl -X GET http://localhost:8000/api/execute/EXECUTION_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Telegram Bot

1. **Start the bot**: Send `/start` to your bot
2. **Create a workflow**: Just describe what you want:
   - "Summarize this text: [your text here]"
   - "Make an HTTP request to get a random joke"
   - "Generate a welcome message for new users"
3. **Execute**: Click the "▶️ Execute Now" button
4. **View results**: See the output directly in Telegram

## 🔧 Verification

Run the verification script to test the backend:
```bash
python verify_backend.py
# OR
uv run python verify_backend.py
```

This will test:
- User registration and login
- Workflow generation
- Workflow execution
- API authentication

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.12
- **Database**: MongoDB (Motor async driver)
- **AI**: Google Gemini API (google-genai SDK)
- **Authentication**: JWT with argon2 password hashing
- **Telegram**: python-telegram-bot
- **HTTP Client**: httpx

## 📝 API Endpoints

### Users
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get JWT token
- `GET /api/users/me` - Get current user info

### Workflows
- `GET /api/workflows` - List user's workflows
- `POST /api/workflows` - Create a workflow manually
- `POST /api/workflows/generate` - Generate workflow from natural language
- `GET /api/workflows/{id}` - Get workflow details
- `PUT /api/workflows/{id}` - Update a workflow
- `DELETE /api/workflows/{id}` - Delete a workflow

### Execution
- `POST /api/execute/{workflow_id}` - Execute a workflow
- `GET /api/execute/{execution_id}` - Get execution status
- `GET /api/execute/workflow/{workflow_id}` - List all executions for a workflow

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- FastAPI for the excellent web framework
- MongoDB for flexible data storage
- python-telegram-bot for Telegram integration

## 📧 Contact

For questions or support, please open an issue on GitHub.
 - Workflow Automation System

A sophisticated workflow automation platform that leverages artificial intelligence to create and execute automated workflows through a Telegram bot interface. The system currently uses Google's Gemini API for natural language processing, with plans to integrate LangChain and OpenAI technologies in the future to enhance workflow generation and tool orchestration capabilities.

## Table of Contents
- [Documentation](#-documentation)
- [Features](#-features)
- [Architecture Overview](#️-architecture)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Development](#-development)
- [Security](#-security)
- [Monitoring](#-monitoring)
- [Contributing](#-contributing)
- [Support](#-support)

## Documentation

### System Documentation
- **[Architecture Documentation](architecture.html)** - Interactive system architecture diagrams and detailed component breakdown
  - System component interactions
  - Data flow visualizations
  - Configuration specifications
  - Security implementation details
  - Monitoring and logging setup

## Features

### Core Capabilities
- **Natural Language Processing**
  - Intuitive workflow creation through conversation
  - Context-aware command interpretation
  - Adaptive response generation

### Interface & Integration
- **Telegram Bot Interface**
  - User-friendly command system
  - Interactive workflow management
  - Real-time execution monitoring

### Automation Features
- **Workflow Management**
  - Automated task execution
  - Sequential and parallel workflow support
  - Error handling and recovery
  - Execution history tracking

### Tool Integration
- **Email Operations**
  - Send and receive emails
  - Attachment handling
  - Template support

- **File System Operations**
  - File creation and manipulation
  - Directory management
  - File transfer capabilities

- **Web Integration**
  - Web scraping
  - API interactions
  - Data extraction

### Security & Monitoring
- **Security Features**
  - JWT authentication
  - Role-based access control
  - Encrypted communications

- **System Monitoring**
  - Real-time logging
  - Performance metrics
  - Error tracking
  - Health monitoring

## Architecture

The system implements a microservices architecture with three primary components:

### 1. Telegram Bot Service (`telegram_bot/`)
- **User Interaction Layer**
  - Command processing
  - Message handling
  - Callback management
  - User session management

- **API Integration**
  - Backend communication
  - Response formatting
  - Error handling

### 2. Backend API (`backend/`)
- **Core Services**
  - FastAPI-based REST endpoints
  - Workflow orchestration
  - User authentication
  - Data persistence

- **Business Logic**
  - Workflow validation
  - Task scheduling
  - Error management
  - State management

### 3. AI Service
- **Current Implementation**
  - Google Gemini API Integration
    - Text processing
    - Command interpretation
    - Response generation

- **Planned Future Implementation with LangChain**
  - Natural language understanding
  - Workflow generation
  - Context management
  - Tool selection and orchestration

## 🚀 Getting Started

### System Requirements
- Python 3.8 or higher
- Docker Engine 20.10.x or higher
- Docker Compose 2.x or higher
- 4GB RAM minimum
- 10GB available disk space

### Prerequisites
1. **API Keys**
   - Telegram Bot Token (from [@BotFather](https://t.me/botfather))
   - OpenAI API Key (from [OpenAI Platform](https://platform.openai.com))
   - Google Gemini API Key (from [Google AI Studio](https://makersuite.google.com))
   > Note: You can use either OpenAI or Gemini as your primary AI provider, or both for different capabilities.

2. **Software Dependencies**
   - MongoDB 4.4+
   - Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Abhinavexists/Relay.git
   cd Relay
   ```

2. **Environment Configuration**

   Option 1: Using the example file (if available)
   ```bash
   cp env-example.txt .env
   ```

   Option 2: Creating .env file from scratch
   ```bash
   # Create .env file
   touch .env
   
   # Open with your preferred editor (e.g., nano, vim, or any text editor)
   nano .env
   ```

   Add the following configuration to your `.env` file:
   ```bash
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000

   # Database Configuration
   MONGODB_URI=mongodb://mongodb:27017
   MONGODB_DB_NAME=workflow_automation

   # Bot Configuration
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

   # AI Service Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here    # (Current Implementation works on this)
   
   # Security Configuration
   SECRET_KEY=your-secret-key-for-jwt
   DEBUG=true
   ```

   > **Important Notes for .env Configuration:**
   > - Replace all placeholder values (e.g., `your_telegram_bot_token_here`) with your actual API keys
   > - Keep this file secure and never commit it to version control
   > - Make sure there are no spaces around the '=' sign
   > - Don't use quotes around values unless they contain spaces
   > - Each value should be on a new line

   To generate a secure SECRET_KEY, you can use this Python command:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Deployment Options

#### Docker Deployment (Recommended)
1. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```

2. **Service Access**
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - MongoDB: `mongodb://localhost:27017`
   - Telegram Bot: Access through Telegram app

#### Manual Deployment
1. **Virtual Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Services**
   ```bash
   # MongoDB
   mongod

   # Backend API
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Telegram Bot
   cd telegram_bot
   python main.py
   ```

## 📱 Usage Guide

### Telegram Bot Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and get welcome message | `/start` |
| `/help` | Display available commands and usage | `/help` |
| `/login` | Authenticate with the system | `/login` |
| `/workflows` | List all your workflows | `/workflows` |
| `/create` | Start workflow creation process | `/create daily report` |

### Workflow Creation
1. Start with `/create` command
2. Describe your workflow in natural language
3. Review and confirm the generated workflow
4. Test the workflow execution
5. Save or modify as needed

### Workflow Management
- List workflows using `/workflows`
- Select workflows for execution
- Monitor execution progress
- View execution history
- Modify or delete workflows

## 🔧 Development

### Project Structure
```
workflow-automation/
├── backend/                 # Backend API service
│   ├── api/                 # API endpoints
│   │   ├── routes/          # Route definitions
│   │   └── middleware/      # Request/response middleware
│   ├── core/                # Core business logic
│   │   ├── tools/           # Automation tools
│   │   └── workflows/       # Workflow management
│   ├── models/              # Data models
│   └── services/            # Service implementations
├── telegram_bot/            # Telegram bot service
│   ├── handlers/            # Command & message handlers
│   │   ├── commands/        # Bot commands
│   │   └── callbacks/       # Inline keyboard handlers
│   ├── utils/               # Utility functions
│   └── config.py            # Bot configuration
├── docker/                  # Docker configuration
│   ├── backend/             # Backend service Dockerfile
│   └── bot/                 # Bot service Dockerfile
├── docs/                    # Additional documentation
├── tests/                   # Test suites
├── docker-compose.yml       # Service orchestration
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── architecture.html        # Interactive architecture docs
```

### Development Guidelines
1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document functions and classes
   - Write unit tests

2. **Feature Development**
   - Create feature branch from `develop`
   - Implement changes
   - Add tests
   - Update documentation
   - Submit pull request

3. **Testing**
   - Run unit tests: `pytest tests/`
   - Check code coverage
   - Perform integration testing
   - Test bot commands manually

## Security

### Authentication
- JWT-based token authentication
- Secure token storage
- Regular token rotation
- Session management

### Authorization
- Role-based access control (RBAC)
- Permission management
- Resource access control
- API endpoint protection

### Data Protection
- Environment variable encryption
- Secure communication channels
- Input validation and sanitization
- Data encryption at rest

## Monitoring

### Application Monitoring
- Detailed application logs
- Error tracking and reporting
- Performance metrics
- User activity monitoring

### System Metrics
- Service health checks
- Resource utilization
- Response times
- Error rates

### Alerting
- Service failure notifications
- Performance degradation alerts
- Security incident alerts
- Custom alert thresholds

## Contributing

### Contribution Process
1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add/update tests
5. Update documentation
6. Submit pull request

### Pull Request Guidelines
- Clear description of changes
- Reference related issues
- Include test results
- Update documentation
- Follow code style guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Technologies
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Google Gemini](https://ai.google.dev/) - Current AI provider
- [LangChain](https://www.langchain.com/) - Planned future AI orchestration
- [OpenAI](https://openai.com/) - Planned future AI capabilities
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram integration
- [MongoDB](https://www.mongodb.com/) - Database system

### Additional Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Docker Documentation](https://docs.docker.com/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)

## Support

### Getting Help
- Open an issue in the GitHub repository
- Contact the maintainers
- Join our community channels

## Primary Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Abhinavexists">
        <img src="https://github.com/Abhinavexists.png" width="100px;" alt="Abhinavexists"/>
        <br />
        <sub><b>Abhinavexists</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ishi-ta-lal">
        <img src="https://github.com/ishi-ta-lal.png" width="100px;" alt="ishi-ta-lal"/>
        <br />
        <sub><b>ishi-ta-lal</b></sub>
      </a>
    </td>
  </tr>
</table>

### Reporting Issues
- Use the issue template
- Provide reproduction steps
- Include relevant logs
- Specify environment details
