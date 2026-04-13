#!/bin/bash
echo "Installing Ollama Agent Dashboard..."
git clone https://github.com/YOURNAME/ollama-agent-dashboard
cd ollama-agent-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Done! Run: source venv/bin/activate && uvicorn main:app --reload"