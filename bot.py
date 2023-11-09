from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChat
import logging
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

logging.warning("Starting...")

APP_ID = int(os.getenv("APP_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
TO = os.getenv("TO_CHANNEL")
KEYWORD_ = "Цветы Цветов Букет Букеты Букетов Розы Роза Пионы Пион Гортензии Гортензия Елка Ель Шарики Подарок Подарки " \
           "День рождение День рождения Свадьба Игрушка Игрушки Сладости Др Праздник Декорации Торт Тортик Панкейк " \
           "Бенто Bento Розы Роза Тюльпаны Тюльпан  Лютик Лютики Цветочный  Флористика"
KEYWORD = [str(i) for i in KEYWORD_.lower().split()]

try:
    client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH, system_version='4.16.30-vxCUSTOM')
    client.start()
except Exception as ap:
    logging.error(f"ERROR - {ap}")
    exit(1)


async def prepare_link(event):
    if event.is_group:
        entity = await client.get_entity(PeerChat(abs(event.message.chat_id)))
        return f'\n\n Переслано из чата {entity.title}'
    chat_title = event.chat.title
    user_id = event.chat.username
    telegram_link = f'https://t.me/{user_id}/{event.message.id}'
    return f'\n\n Переслано из [{chat_title}]({telegram_link})'


@client.on(events.NewMessage(incoming=True))
async def sender_client(event):
    if event.is_group or event.is_channel:
        event_message = event.message.message
        for substr in KEYWORD:
            if substr in event_message.lower():
                entity = await client.get_input_entity(TO)
                link = await prepare_link(event)
                message = f'#{substr}\n\n' + event_message + link
                try:
                    await client.send_message(entity, message, link_preview=False)
                except Exception as e:
                    logging.error(e)

logging.warning("Bot has started.")
client.run_until_disconnected()
