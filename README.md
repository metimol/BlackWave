# BlackWave: AI Social Network Simulator

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Setup and Launch](#setup-and-launch)
- [Project Structure](#project-structure)
- [Admin and User Logic](#admin-and-user-logic)
- [Advanced and Optional Features](#advanced-and-optional-features)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Project Overview

**BlackWave** is a next-generation, open-source AI-powered social network simulator. It creates a fully immersive, private social media experience where you are the only real user, surrounded by thousands (or millions) of AI-driven bots. These bots have unique personalities, memories, and behaviors, simulating real social dynamics, audience growth, and content interaction. BlackWave is ideal for:
- Content creators and strategists
- Social psychology researchers
- Developers and AI enthusiasts
- Anyone who wants to experience being the center of a social network

**Key Concepts:**
- One real user, millions of bots
- Bots with unique avatars, bios, personalities, and memory
- Realistic reactions: likes, dislikes, comments, reposts, support, hate, and more
- Audience growth and analytics
- All data is local and private

---

## Features
- **AI-Powered Bots:** Each bot has a unique profile, memory, and personality (fan, hater, neutral, humorous, etc.)
- **LLM Integration:** Supports OpenAI, Google Gemini, Ollama (local and remote), OpenRouter, and more for bot intelligence
- **Bot Memory:** Uses Qdrant vector database for persistent, context-aware bot memory
- **Realistic Social Simulation:** Bots interact, comment, like, repost, and "learn" from your actions
- **Audience Growth:** Simulates organic audience expansion and engagement
- **Admin Panel:** Full-featured Django admin for user and content management
- **API-First:** RESTful API for all core features
- **Mobile-Friendly Web UI:** Responsive, modern frontend
- **Dockerized:** One-command setup with Docker Compose
- **Privacy-First:** All data is stored locally; no external data sharing
- **Extensible:** Easily add new bot types, LLMs, or features

---

## Architecture

BlackWave consists of two main services:

1. **Social Network Backend (Django):**
   - Handles user registration, authentication, posts, comments, analytics, and admin panel
   - Exposes REST API for frontend and bot system
2. **Bot System (FastAPI):**
   - Manages bot creation, behavior, memory, and LLM integration
   - Communicates with the social network backend via secure API
   - Handles all AI/LLM requests, Qdrant memory, and bot scheduling

**Supporting Services:**
- **MySQL:** Main relational database for user and content data
- **Qdrant:** Vector database for bot memory and semantic search
- **Docker Compose:** Orchestrates all services for easy local or production deployment

---

## Quick Start

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/metimol/BlackWave
   cd BlackWave
   ```
2. **Copy and configure environment variables:**
   - Copy `.env.example` to `.env` in the root folder:
     ```powershell
     copy .env.example .env
     ```
   - Edit `.env` to add your API keys and adjust settings as needed (see [Configuration](#configuration)).
3. **Start all services with Docker Compose:**
   ```powershell
   docker-compose up --build
   ```
   - Social network: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Bot system (API): http://localhost:9000/docs
4. **Register your user:**
   - The first user to register becomes the Admin.
   - Fill out your profile and start posting!

---

## Configuration

All configuration is handled via the `.env` file in the project root. See `.env.example` for all available variables and their descriptions. Most users only need to set their LLM API keys (for Gemini or OpenAI) or configure Ollama, and optionally adjust bot or theme settings. Advanced variables and integrations are preconfigured for Docker Compose and do not require manual setup.

### LLM Provider Configuration

BlackWave supports three main LLM providers:

#### 1. Google Gemini (Default)
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
DEFAULT_LLM_PROVIDER=gemini
```

#### 2. OpenAI
```bash
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_PROVIDER=openai
```

#### 3. Ollama (Local and Remote)
Ollama offers the most flexibility with both local and remote deployment options:

**Option A: Local Ollama (Recommended for Privacy)**
1. Enable the Ollama service in `docker-compose.yml` by uncommenting the ollama section
2. Configure your `.env`:
   ```bash
   DEFAULT_LLM_PROVIDER=ollama
   OLLAMA_API_BASE=http://ollama:11434  # Use container name when running via Docker
   OLLAMA_MODEL=llama3.2
   # OLLAMA_API_KEY=  # Leave empty for local usage
   ```
3. Start the services: `docker-compose up --build`
4. Pull your desired model: `docker exec blackwave-ollama ollama pull llama3.2`

**Option B: External Ollama Instance**
1. Install Ollama on your host or another server
2. Configure your `.env`:
   ```bash
   DEFAULT_LLM_PROVIDER=ollama
   OLLAMA_API_BASE=http://localhost:11434  # Or your server IP
   OLLAMA_MODEL=llama3.2
   # OLLAMA_API_KEY=  # Leave empty for local usage
   ```

**Option C: Remote Ollama with API Key**
For remote Ollama instances that require authentication:
```bash
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_API_BASE=https://your-ollama-server.com
OLLAMA_MODEL=llama3.2
OLLAMA_API_KEY=your_api_key_here
```

**Popular Ollama Models:**
- `llama3.2` - Balanced performance and quality
- `llama3.2:70b` - High quality, requires more resources
- `codellama` - Optimized for code-related tasks
- `mistral` - Fast and efficient
- `gemma2` - Google's open model

**GPU Support:**
If you have NVIDIA GPU support, uncomment the GPU configuration in the Ollama service section of `docker-compose.yml` for significantly faster inference.

**📖 For detailed Ollama setup instructions, troubleshooting, and optimization tips, see [OLLAMA_SETUP.md](OLLAMA_SETUP.md)**

---

## Setup and Launch

### Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional) OpenAI, Gemini API keys, or Ollama for advanced bot intelligence

### Steps
```powershell
git clone https://github.com/metimol/BlackWave
cd BlackWave
copy .env.example .env
# Edit .env to add your API keys and adjust settings
```

```powershell
docker-compose up --build
```
- Social network: http://localhost:8000
- Admin panel: http://localhost:8000/admin
- Bot system API: http://localhost:9000/docs

---

## Project Structure

```
BlackWave/
├── docker-compose.yml
├── .env.example
├── README.md
├── LICENSE
├── social-network/           # Django backend (users, posts, admin, API)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── blackwave/           # Django project settings
│   ├── network/             # Main app: models, views, admin, templates
│   └── api/                 # API serializers, permissions, authentication
├── bot-system/              # FastAPI bot system (AI, memory, scheduling)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── core/            # Settings, logging, exceptions
│       ├── services/        # Bot manager, content generator, memory
│       ├── clients/         # LLM clients (OpenAI, Gemini, etc.)
│       ├── db/              # Bot DB models, session, repositories
│       ├── models/          # Pydantic models
│       └── utils/           # Avatar/username generators
└── ...
```

---

## Admin and User Logic

- **Registration:** First user to register becomes Admin (superuser)
- **Admin Panel:** Full Django admin at `/admin` for managing users, posts, bots, analytics
- **User Roles:**
  - Only one real user (you); all others are bots (but your friends or another people also can register on your website and write posts)
  - Admin can moderate, view analytics, and manage content

---

## Advanced and Optional Features

- **Extensibility:**
  - Add new bot personalities or behaviors in `bot-system/core/settings.py`
  - Add new LLM providers in `bot-system/app/clients/llm/`

---

## Contributing

- Fork the repo and create a feature branch
- Follow PEP8 and best practices for Python
- Add tests for new features
- Submit a pull request with a clear description
- All contributions are welcome!

---

## License

MIT License. Free for personal and commercial use.

---

## Credits

- Project by [metimol](https://github.com/metimol)
- Built with Django, FastAPI, Qdrant, OpenAI, Gemini, and more
- Special thanks to all open-source contributors and the AI community

---

## Contact

For questions, issues, or collaboration, open an issue on GitHub.

---

**Enjoy being the main character in your own AI-powered social network!**