import logging
import os

from telegram import Bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def setup_telegram(token: str, server_url: str) -> bool:
    try:
        bot = Bot(token=token)
        webhook_url = f"{server_url}/webhook/{token}"
        current_webhook = await bot.get_webhook_info()
        if current_webhook.url == webhook_url:
            logger.info("Webhook ya configurado.")
            return True
        logger.info(f"Configurando webhook: {webhook_url}")
        await bot.delete_webhook()
        await bot.set_webhook(webhook_url)
        return True
    except Exception as e:
        logger.error(f"Error configurando webhook: {str(e)}")
        return False

def setup_ngrok():
    from pyngrok import ngrok, conf
    NGROK_TOKEN = os.environ.get('NGROK_TOKEN')
    conf.get_default().auth_token = NGROK_TOKEN
    ngrok_tunel = ngrok.connect(8000, bind_tls=True)
    server_url = ngrok_tunel.public_url
    return server_url