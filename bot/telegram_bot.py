from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackContext

from ai.graph_bot import GraphBot


class TelegramBot:

    def __init__(self, token: str, store, checkpointer):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.graph = GraphBot(store=store, checkpointer=checkpointer)
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button))
        text_handler = MessageHandler(filters.TEXT, self.handle_text_message)
        self.app.add_handler(text_handler)
        self.app.add_handler(CommandHandler("help", self.help_command))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hola bienvenido.")

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query.data}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Use /start to test this bot.")

    async def handle_text_message(self, update: Update, context: CallbackContext):
        message_tg = update.message
        chat_tg = update.effective_chat
        user_tg = update.effective_user
        response = await self.graph.reply(
            chat_id=chat_tg.id,
            user_id=user_tg.id,
            text=message_tg.text,
        )
        await message_tg.reply_text(response)
