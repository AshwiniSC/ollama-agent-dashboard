# Ollama Agent Dashboard

A local AI agent dashboard for Ollama. Create, manage and chat with custom AI agents — 100% private, runs on your machine.

## Features
- Create custom agents with system prompts
- Supports all Ollama models
- Chat history per session
- Zero cloud, zero data sharing

## Install
git clone https://github.com/YOURNAME/ollama-agent-dashboard
cd ollama-agent-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

## Requirements
- Python 3.8+
- Ollama running locally (https://ollama.ai)