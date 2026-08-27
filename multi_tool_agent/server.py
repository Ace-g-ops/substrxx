from fastapi import FASTAPI
from google.adk.cli.fast_api import get_fast_api_app
from agent import app

fastapi_app: FASTAPI = get_fast_api_app(
    agents=[app.root_agent],
    web = True,
) 

fastapi_app.mount("/agent", app.interface()) ## this mounts the app with caching and other features provided by the App class

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)



