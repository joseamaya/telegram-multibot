from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from telegram import Update

from dependencies import bot_manager

router = APIRouter()

@router.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    bot = bot_manager.get_bot(token)
    if not bot:
        return JSONResponse(content={"status": "error", "message": "Bot not found"}, status_code=404)

    update = Update.de_json(await request.json(), bot.app.bot)
    await bot.app.process_update(update)
    return JSONResponse(content={"status": "ok"})
