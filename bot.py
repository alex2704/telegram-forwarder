from telethon import TelegramClient, events
from telethon.sessions import StringSession
import logging
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

logging.warning("Starting...")

APP_ID = int(os.getenv("APP_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
TO = os.getenv("TO_CHANNEL")
KEYWORD_ = "цветы цветов"
KEYWORD = [str(i) for i in KEYWORD_.split()]

try:
    client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH, system_version='4.16.30-vxCUSTOM')
    client.start()
except Exception as ap:
    logging.error(f"ERROR - {ap}")
    exit(1)


@client.on(events.NewMessage(incoming=True))
async def sender_client(event):
    if event.is_group or event.is_channel:
        event_message = event.message.message
        for substr in KEYWORD:
            if substr in event_message:
                entity = await client.get_input_entity(TO)
                user_id = event.chat.username
                chat_title = event.chat.title
                telegram_link = f'tg://openmessage?chat_id={user_id}&message_id={event.message.id}'
                # telegram_link = f'https://t.me/{user_id}/{event.message.id}'
                message = f'#{substr}\n\n' + event_message + f'\n\n Переслано из [{chat_title}]({telegram_link})'
                try:
                    await client.send_message(entity, message, link_preview=False)
                except Exception as e:
                    logging.error(e)

logging.warning("Bot has started.")
client.run_until_disconnected()
