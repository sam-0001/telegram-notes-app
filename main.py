from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
import uvicorn
import os

from . import models
from .database import engine, get_db
from .routers import users, files
from .services.telegram_bot import handle_telegram_update, set_telegram_webhook

# Create all database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Notes Management System")

# Set up Telegram webhook on application startup
@app.on_event("startup")
async def startup_event():
    await set_telegram_webhook()

# Include API routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])

# Root endpoint
@app.get("/")
def read_root():
    return {"status": "API is running"}

# Webhook endpoint for Telegram to send updates to
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    update_data = await request.json()
    await handle_telegram_update(update_data, db)
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
