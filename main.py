from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import json
import os

app = FastAPI()

AGENTS_FILE = "agents.json"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Load/save agents
def load_agents():
    if not os.path.exists(AGENTS_FILE):
        return {}
    with open(AGENTS_FILE) as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_agents(agents):
    with open(AGENTS_FILE, "w") as f:
        json.dump(agents, f, indent=2)

# Models
class AgentCreate(BaseModel):
    name: str
    system_prompt: str
    model: str = "llama3"

class ChatRequest(BaseModel):
    agent_name: str
    message: str
    history: list = []

# Routes
@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/agents")
def get_agents():
    return load_agents()

@app.post("/agents")
def create_agent(agent: AgentCreate):
    agents = load_agents()
    agents[agent.name] = {
        "system_prompt": agent.system_prompt,
        "model": agent.model
    }
    save_agents(agents)
    return {"status": "created", "agent": agent.name}

@app.delete("/agents/{name}")
def delete_agent(name: str):
    agents = load_agents()
    if name in agents:
        del agents[name]
        save_agents(agents)
    return {"status": "deleted"}

@app.post("/chat")
async def chat(req: ChatRequest):
    agents = load_agents()
    if req.agent_name not in agents:
        return {"error": "Agent not found"}
    
    agent = agents[req.agent_name]
    
    messages = [{"role": "system", "content": agent["system_prompt"]}]
    messages += req.history
    messages.append({"role": "user", "content": req.message})
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": agent["model"],
            "messages": messages,
            "stream": False
        })
        data = response.json()
        reply = data["message"]["content"]
    
    return {"reply": reply}

@app.get("/models")
async def get_models():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:11434/api/tags")
        data = response.json()
        models = [m["name"] for m in data.get("models", [])]
    return {"models": models}

app.mount("/static", StaticFiles(directory="static"), name="static")