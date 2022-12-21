import asyncio
import datetime as dt
import random
import string
from telethon import TelegramClient, events
from telethon.sessions import MemorySession
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors.rpcerrorlist import UsernameNotModifiedError, UsernameInvalidError, UsernameOccupiedError, FloodWaitError


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


# Auto changes my username whenever I trigger the command
@client.on(events.NewMessage(outgoing=True, pattern='!change'))
async def change_username_handler(event):
    try:
        print('trigger change username')
        characters = string.ascii_letters + string.digits
        username = ''.join(random.choice(characters) for i in range(15))
        await client(UpdateUsernameRequest(username=username))
    except (UsernameNotModifiedError, UsernameInvalidError, UsernameOccupiedError, FloodWaitError) as e:
        pass


# Auto delete messages after 1 hour
@client.on(events.NewMessage())
async def self_delete_handler(event):
    sender = await event.get_sender()
    me = await client.get_me()
    if sender.username == me.username:
        print('delete event scheduled')
        await asyncio.sleep(3600)
        await event.delete()


if __name__ == '__main__':
    print('telegram master started at {time}'.format(time=dt.datetime.now()))
    client.start()
    client.run_until_disconnected()
    print('telegram master ended at {time}'.format(time=dt.datetime.now()))
