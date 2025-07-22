# Ollama Setup Guide for BlackWave

This guide covers all aspects of setting up Ollama with BlackWave, from local installation to remote deployment with API keys.

## Table of Contents
- [What is Ollama?](#what-is-ollama)
- [Setup Options](#setup-options)
- [Local Docker Setup (Recommended)](#local-docker-setup-recommended)
- [External Ollama Setup](#external-ollama-setup)
- [Remote Ollama with API Key](#remote-ollama-with-api-key)
- [Model Management](#model-management)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## What is Ollama?

Ollama is a tool that allows you to run large language models locally on your machine or server. It provides:

- **Privacy**: All data stays on your machine
- **No API costs**: Free to use once set up
- **Offline capability**: Works without internet connection
- **Model variety**: Support for many open-source models
- **GPU acceleration**: Faster inference with compatible hardware

## Setup Options

BlackWave supports three Ollama deployment scenarios:

1. **Local Docker** (Recommended) - Ollama runs as a Docker container alongside BlackWave
2. **External Instance** - Ollama runs on your host machine or another server
3. **Remote with API Key** - Connect to a remote Ollama instance that requires authentication

## Local Docker Setup (Recommended)

This is the easiest way to get started with Ollama and BlackWave.

### Step 1: Enable Ollama in Docker Compose

Edit `docker-compose.yml` and uncomment the Ollama service section:

```yaml
  ollama:
    image: ollama/ollama:latest
    container_name: blackwave-ollama
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - blackwave-network
    restart: unless-stopped
```

Also uncomment the volume:
```yaml
volumes:
  # ... other volumes
  ollama_data:
    driver: local
```

### Step 2: Configure Environment Variables

Update your `.env` file:

```bash
# LLM Configuration
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_API_BASE=http://ollama:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=60
# OLLAMA_API_KEY=  # Leave empty for local usage
```

### Step 3: Start Services

```bash
docker-compose up --build
```

### Step 4: Pull a Model

Once the services are running, pull your desired model:

```bash
# Pull the default model
docker exec blackwave-ollama ollama pull llama3.2

# Or pull a different model
docker exec blackwave-ollama ollama pull mistral
```

### Step 5: Verify Setup

Check that the model is available:

```bash
docker exec blackwave-ollama ollama list
```

You should see your pulled model listed.

## External Ollama Setup

If you prefer to run Ollama on your host machine or another server:

### Step 1: Install Ollama

**On Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**On Windows:**
Download from [https://ollama.ai/download](https://ollama.ai/download)

### Step 2: Start Ollama Service

```bash
ollama serve
```

### Step 3: Pull a Model

```bash
ollama pull llama3.2
```

### Step 4: Configure BlackWave

Update your `.env` file:

```bash
# LLM Configuration
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_API_BASE=http://localhost:11434  # Or your server IP
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=60
# OLLAMA_API_KEY=  # Leave empty for local usage
```

### Step 5: Start BlackWave

```bash
docker-compose up --build
```

## Remote Ollama with API Key

For remote Ollama instances that require authentication:

### Step 1: Configure Environment Variables

Update your `.env` file:

```bash
# LLM Configuration
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_API_BASE=https://your-ollama-server.com
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=60
OLLAMA_API_KEY=your_api_key_here
```

### Step 2: Start BlackWave

```bash
docker-compose up --build
```

## Model Management

### Popular Models and Their Use Cases

| Model | Size | Use Case | Performance |
|-------|------|----------|-------------|
| `llama3.2` | ~4.7GB | General purpose, balanced | Good |
| `llama3.2:70b` | ~40GB | High quality responses | Excellent |
| `mistral` | ~4.1GB | Fast, efficient | Good |
| `codellama` | ~3.8GB | Code generation | Good for code |
| `gemma2` | ~5.4GB | Google's open model | Good |
| `phi3` | ~2.3GB | Lightweight, fast | Fair |

### Pulling Models

```bash
# For Docker setup
docker exec blackwave-ollama ollama pull model_name

# For external setup
ollama pull model_name
```

### Listing Available Models

```bash
# For Docker setup
docker exec blackwave-ollama ollama list

# For external setup
ollama list
```

### Removing Models

```bash
# For Docker setup
docker exec blackwave-ollama ollama rm model_name

# For external setup
ollama rm model_name
```

## Performance Optimization

### GPU Support (NVIDIA)

For significantly faster inference, enable GPU support:

1. Install [NVIDIA Docker runtime](https://github.com/NVIDIA/nvidia-docker)

2. Uncomment GPU configuration in `docker-compose.yml`:

```yaml
  ollama:
    # ... other config
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

3. Restart the services:

```bash
docker-compose down
docker-compose up --build
```

### Memory Management

- **Small models (2-4GB)**: Work well on 8GB+ RAM systems
- **Medium models (4-8GB)**: Require 16GB+ RAM
- **Large models (40GB+)**: Need 64GB+ RAM or GPU with sufficient VRAM

### CPU Optimization

Ollama automatically uses available CPU cores. For better performance:

- Ensure adequate RAM
- Use SSD storage for model files
- Close unnecessary applications

## Troubleshooting

### Common Issues

#### 1. "Connection refused" error

**Problem**: BlackWave can't connect to Ollama

**Solutions**:
- Ensure Ollama service is running
- Check `OLLAMA_API_BASE` URL is correct
- For Docker setup, use `http://ollama:11434`
- For external setup, use `http://localhost:11434`

#### 2. "Model not found" error

**Problem**: The specified model isn't available

**Solutions**:
```bash
# Check available models
docker exec blackwave-ollama ollama list

# Pull the required model
docker exec blackwave-ollama ollama pull llama3.2
```

#### 3. Slow response times

**Problem**: Model responses are very slow

**Solutions**:
- Use a smaller model (e.g., `phi3` instead of `llama3.2:70b`)
- Enable GPU support if available
- Increase `OLLAMA_TIMEOUT` value
- Ensure sufficient RAM

#### 4. Out of memory errors

**Problem**: System runs out of memory

**Solutions**:
- Use a smaller model
- Close other applications
- Increase system swap space
- Use GPU with sufficient VRAM

### Debugging Commands

```bash
# Check Ollama container logs
docker logs blackwave-ollama

# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Test model generation
docker exec blackwave-ollama ollama run llama3.2 "Hello, world!"
```

### Performance Monitoring

Monitor resource usage while running:

```bash
# Check container resource usage
docker stats blackwave-ollama

# Monitor system resources
htop
```

## Best Practices

1. **Start with smaller models** like `llama3.2` or `mistral`
2. **Use GPU acceleration** when available
3. **Monitor memory usage** and choose models accordingly
4. **Keep models updated** by occasionally pulling newer versions
5. **Use appropriate timeouts** for your hardware capabilities

## Support

If you encounter issues:

1. Check the [Ollama documentation](https://github.com/ollama/ollama)
2. Review BlackWave logs: `docker logs blackwave-bot-service`
3. Open an issue on the BlackWave GitHub repository

---

**Enjoy running BlackWave with complete privacy using Ollama!**