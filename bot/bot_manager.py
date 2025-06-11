from typing import Dict

from ai.store import get_store
from bot.telegram_bot import TelegramBot


class BotManager:

    def __init__(self):
        self.bots: Dict[str, TelegramBot] = {}

    def add_bot(self, token: str) -> TelegramBot:
        if token not in self.bots:
            self.bots[token] = TelegramBot(token)
        return self.bots[token]

    def get_bot(self, token: str) -> TelegramBot:
        return self.bots.get(token)

    async def initialize_all(self):
        for bot in self.bots.values():
            await bot.app.initialize()
            await bot.app.start()

    async def shutdown_all(self):
        for bot in self.bots.values():
            await bot.app.stop()
            await bot.app.shutdown()