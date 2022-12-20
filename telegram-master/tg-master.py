import asyncio
import datetime as dt
import random
import string
from telethon import TelegramClient, events
from telethon.sessions import MemorySession
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors.rpcerrorlist import UsernameNotModifiedError, UsernameInvalidError, UsernameOccupiedError


# credentials
api_id = 17377816
api_hash = '1d7c81bf09b72bf151a4cc67471fc64f'
phone = '+88805413186'


client = TelegramClient(MemorySession(), api_id, api_hash)


# Auto greetings to private chats
@client.on(events.NewMessage(pattern='(?i)hi|hello'))
async def greetings_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        await event.respond('hi {name}, how are you?'.format(name=sender.username))


# Auto delete messages after 10 minutes
@client.on(events.NewMessage())
async def self_delete_handler(event):
    sender = await event.get_sender()
    me = await client.get_me()
    if sender.username == me.username:
        await asyncio.sleep(600)
        await event.delete()


# Auto changes my username whenever there's a message
@client.on(events.NewMessage())
async def change_username_handler(event):
    try:
        characters = string.ascii_letters + string.digits
        username = ''.join(random.choice(characters) for i in range(10))
        await client(UpdateUsernameRequest(username=username))
    except (UsernameNotModifiedError, UsernameInvalidError, UsernameOccupiedError) as e:
        pass


if __name__ == '__main__':
    print('telegram master started at {time}'.format(time=dt.datetime.now()))
    client.start()
    client.run_until_disconnected()
    print('telegram master ended at {time}'.format(time=dt.datetime.now()))
