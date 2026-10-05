import os
import sys
import uvicorn
from fastapi import FastAPI

# Add project root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase AI Legal Document Generator")

# Include API routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}

if __name__ == "__main__":
    uvicorn.run("legalEaseAPI.main:app", host="0.0.0.0", port=8000, reload=True)
