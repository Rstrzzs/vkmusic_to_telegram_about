from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import nest_asyncio

nest_asyncio.apply()

api_id = "API_ID"
api_hash = 'API_HASH'
t_number = "PHONE_NUMBER"

client = TelegramClient('anon', api_id, api_hash,system_version="4.16.30-vxCUSTOM")

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()

        return info.artist, info.title
async def check():
    while True:
        artist = await get_media_info()
        title = await get_media_info()
        print(f"Artist: {artist}, Song: {title}")
        return artist

async def main():
    while True:
        artist = await get_media_info()
        title = await get_media_info()
        print(f"Artist: {artist}, Song: {title}")
        user = await client.get_me()
        fullUser = await client(GetFullUserRequest(user))

        try:
            async with client:
                await client(UpdateProfileRequest(about=f"VK🎵|{artist[0]} - {artist[1]}"))
        except Exception:
            async with client:
                await client(UpdateProfileRequest(about=f"VK🎵|None - None"))

        if fullUser.full_user.about:
            print(user.first_name + " has the following Bio:")
            print(fullUser.full_user.about)
        await asyncio.sleep(90)
        async with client:
            client.loop.run_until_complete(main())

with client:
    client.loop.run_until_complete(main())


