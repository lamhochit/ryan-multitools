import asyncio
import datetime as dt
from telethon import TelegramClient, events
from telethon.sessions import MemorySession


# credentials
api_id = 17377816
api_hash = '1d7c81bf09b72bf151a4cc67471fc64f'


if __name__ == '__main__':
    client = TelegramClient(MemorySession(), api_id, api_hash)

    @client.on(events.NewMessage(pattern='(?i)hi|hello'))
    async def greetings_handler(event):
        sender = await event.get_sender()
        await event.respond('hi {name}, how are you?'.format(name=sender.username))

    print('telegram master started at {time}'.format(time=dt.datetime.now()))
    client.start()
    client.run_until_disconnected()
    print('telegram master ended at {time}'.format(time=dt.datetime.now()))
