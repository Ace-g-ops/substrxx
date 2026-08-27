from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from agent import app 
import os

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

fastapi_app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:fastapi_app", host="0.0.0.0", port=8000)



