# Relay - Workflow Automation System

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

### Reporting Issues
- Use the issue template
- Provide reproduction steps
- Include relevant logs
- Specify environment details
