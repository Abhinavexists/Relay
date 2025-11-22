<div align="center">

# Relay

### AI-Powered Workflow Automation Platform

*Create, manage, and execute complex workflows through natural language - no coding required*

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## What is Relay?

Relay transforms workflow automation by letting you **describe what you want in plain English**. Powered by Google's Gemini AI, it automatically generates and executes workflows - whether you're summarizing documents, making API calls, or orchestrating complex multi-step processes.

### Why Relay?

- **Zero Code Required** - Just describe your workflow in natural language
- **Instant Execution** - Workflows run immediately with real-time feedback
- **AI-Powered** - Gemini AI understands context and generates optimal workflows
- **Telegram Integration** - Manage everything from your phone
- **Secure by Default** - JWT authentication with argon2 password hashing
- **Full Observability** - Track every execution with detailed logs
---

## Quick Start

### Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose** (recommended)
- **Google Gemini API key** ([Get one here](https://makersuite.google.com/app/apikey))
- **Telegram Bot Token** (optional - [Create with @BotFather](https://t.me/botfather))

### Docker Setup (Recommended)

The easiest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/Abhinavexists/Relay.git
cd Relay

# 2. Run the automated setup script
sudo ./scripts/setup.sh

# 3. Configure your environment
# Edit .env file with your API keys (created by setup script)
nano .env

# 4. Start everything with Docker
docker-compose up --build
```

**That's it!** Your Relay instance is now running:

- **API**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>

### Manual Setup (Alternative)

If you prefer not to use Docker:

```bash
# 1. Clone and setup
git clone https://github.com/Abhinavexists/Relay.git
cd Relay

# 2. Use our automated run script
./scripts/run.sh
```

The run script will:

- Create a virtual environment
- Install all dependencies
- Start the backend server
- Handle environment validation

### Environment Configuration

After running the setup, configure your `.env` file:

```env
# Required - Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Database (default works with Docker)
MONGODB_URI=mongodb://mongodb:27017
MONGODB_DB_NAME=workflow_automation

# Security (generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your-secret-key-for-jwt
```

### First Workflow in 30 Seconds

```bash
# Register
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "secure123", "full_name": "Your Name"}'

# Login and get token
TOKEN=$(curl -X POST http://localhost:8000/api/users/login \
  -d "username=you@example.com&password=secure123" | jq -r .access_token)

# Create a workflow from natural language
curl -X POST http://localhost:8000/api/workflows/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Summarize this: AI is transforming how we work and live."}'

# Execute it (replace WORKFLOW_ID with the ID from above)
curl -X POST http://localhost:8000/api/execute/WORKFLOW_ID \
  -H "Authorization: Bearer $TOKEN" -d '{}'
```
---

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=workflow_automation

# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Authentication
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Debug
DEBUG=true
```

### Getting API Keys

1. **Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key to your `.env` file

2. **Telegram Bot Token** (Optional):
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow the instructions
   - Copy the bot token to your `.env` file

3. **JWT Secret Key**:
   - Generate a secure random key:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

---

## Understanding Workflows

### What is a Workflow?

A workflow in Relay is a series of automated actions that execute in a specific order. Each workflow consists of:

- **Trigger**: What starts the workflow (manual, scheduled, webhook, or event)
- **Actions**: Individual tasks to perform (AI operations, API calls, etc.)
- **Edges**: Connections defining the execution order
- **Context**: Data passed between actions

### Workflow Structure

```json
{
  "name": "Example Workflow",
  "description": "Summarizes text using AI",
  "trigger": {
    "type": "manual",
    "config": {}
  },
  "actions": [
    {
      "id": "action_1",
      "name": "Summarize Text",
      "type": "summarize",
      "config": {
        "text": "Long text to summarize..."
      }
    }
  ],
  "edges": []
}
```

### Action Types Explained

| Action Type | Purpose | Example Use Case |
|-------------|---------|------------------|
| `summarize` | Condense long text | Summarize articles, documents |
| `extract` | Pull specific information | Extract names, dates, key facts |
| `classify` | Categorize content | Sentiment analysis, topic classification |
| `generate` | Create new content | Generate emails, responses |
| `http_request` | Call external APIs | Fetch data, trigger webhooks |
| `send_email` | Send emails | Notifications, reports |
| `data_transformation` | Process data | Format conversion, filtering |

### Execution Flow

```
User Request → AI Generates Workflow → Workflow Saved → Execute Workflow
                                                              ↓
                                                    Graph Traversal Engine
                                                              ↓
                                                    Execute Actions in Order
                                                              ↓
                                                    Return Results + Logs
```
---

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/register` | POST | Create new user account |
| `/api/users/login` | POST | Authenticate and get JWT token |
| `/api/workflows/generate` | POST | Generate workflow from natural language |
| `/api/workflows` | GET | List all workflows |
| `/api/execute/{id}` | POST | Execute a workflow |
| `/api/execute/{id}` | GET | Get execution status and results |

### Project Structure

```
Relay/
├── backend/                     # FastAPI application
│   ├── api/routes/              # API endpoints(users, workflows, execution)
│   ├── core/                    # Security, config, and tools
│   ├── database/                # MongoDB connection and utilities
│   ├── models/                  # Pydantic data models
│   ├── services/                # Business logic layer
│   │   ├── ai_service.py        # Gemini AI integration
│   │   ├── tool_service.py      # Action executors (HTTP, email, etc.)
│   │   └── workflow_service.py  # Graph traversal engine
│   └── utils/                   # Helper functions
├── telegram_bot/                # Telegram bot interface
│   ├── handlers/                # Command and message handlers
│   └── utils/                   # API client for backend communication
├── scripts/                     # Automation scripts
│   ├── setup.sh                 # Initial project setup
│   └── run.sh                   # Development server launcher
├── docker/                      # Docker configurations
├── tests/                       # Test suite
├── docker-compose.yml           # Multi-service orchestration
├── verify_backend.py            # End-to-end verification script
├── requirements.txt             # Python dependencies
└── Contributing.md       
```

---

## Examples

### Example 1: Text Summarization via Telegram

```
You: Summarize this text: "Artificial intelligence is transforming 
     how we work and live. Machine learning algorithms can now process 
     vast amounts of data to find patterns and make predictions."

Bot: ✅ I've created a workflow for you!
     📋 Text Summarization Workflow
     
     [▶️ Execute Now] [📊 View Details]

You: *clicks Execute Now*

Bot: ✅ Workflow executed!
     📊 Output:
     • ai_result: AI is revolutionizing work and life through ML 
       algorithms that analyze data for pattern recognition and predictions.
```

### Example 2: API Integration via REST

```python
import requests

# Generate a workflow that fetches a random joke
response = requests.post(
    "http://localhost:8000/api/workflows/generate",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "description": "Make an HTTP request to get a random joke from "
                      "https://official-joke-api.appspot.com/random_joke"
    }
)

workflow_id = response.json()["id"]

# Execute it
result = requests.post(
    f"http://localhost:8000/api/execute/{workflow_id}",
    headers={"Authorization": f"Bearer {token}"},
    json={}
)

print(result.json()["output_data"])
# Output: {"setup": "Why did the chicken cross the road?", ...}
```

### Example 3: Chained Workflow

```bash
# Create a workflow that:
# 1. Fetches data from an API
# 2. Summarizes it with AI
# 3. Sends results via email

curl -X POST http://localhost:8000/api/workflows/generate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Fetch GitHub user data, summarize their bio, 
                    and email the summary to admin@example.com"
  }'
```

---

## Technology Stack

<div align="left">

| Category | Technologies |
|----------|-------------|
| **Backend** | FastAPI, Python 3.12, Pydantic |
| **Database** | MongoDB, Motor (async driver) |
| **AI** | Google Gemini API (google-genai SDK) |
| **Authentication** | JWT, argon2-cffi |
| **Bot** | python-telegram-bot |
| **HTTP** | httpx (async client) |

</div>

---

## Testing

Run the verification script to test all components:

```bash
uv run python verify_backend.py
```

**What it tests:**

- User registration and authentication
- AI workflow generation
- Workflow execution with real actions
- API endpoint security

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](Contributing.md) for detailed information about:


## FAQ

**Q: Do I need a Telegram bot to use Relay?**  
A: No, the Telegram bot is optional. You can use the REST API directly.

**Q: Can I use OpenAI instead of Gemini?**  
A: Currently, only Gemini is supported. OpenAI integration is on the roadmap.

**Q: How do I create custom action types?**  
A: Custom actions aren't supported yet, but it's planned for a future release.

**Q: Is there a limit on workflow executions?**  
A: No built-in limits, but you're subject to Gemini API rate limits.

**Q: Can workflows run on a schedule?**  
A: Scheduled triggers are planned but not yet implemented. Currently, only manual triggers work.

**Q: How do I backup my workflows?**  
A: Workflows are stored in MongoDB. Use `mongodump` to backup:

```bash
mongodump --db workflow_automation --out /path/to/backup
```

**Q: Can I share workflows with other users?**  
A: Not currently. Each user's workflows are private to their account.

**Q: What happens if a workflow action fails?**  
A: The execution stops, and the error is logged. You can view the error in the execution details.

---

## Roadmap

- [ ] **LangChain Integration** - Enhanced AI orchestration
- [ ] **OpenAI Support** - Alternative AI provider
- [ ] **Workflow Scheduler** - Time-based triggers
- [ ] **Web Dashboard** - Visual workflow builder
- [ ] **Webhook Triggers** - Event-driven workflows
- [ ] **Plugin System** - Custom action types
- [ ] **Multi-language Support** - i18n for Telegram bot

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built with amazing open-source technologies:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [Google Gemini](https://ai.google.dev/) - Powerful AI capabilities
- [MongoDB](https://www.mongodb.com/) - Flexible document database
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram integration

---

## � Contributors

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

---