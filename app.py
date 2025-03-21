from fastapi import FastAPI
import os

# Read the app name from environment variable (APPNAME)
app_name = os.getenv("APPNAME", "Yantras")

# Initialize FastAPI app
app = FastAPI()

@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello {name}! I am {app_name}"}
