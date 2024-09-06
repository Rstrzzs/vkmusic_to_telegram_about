import random

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import nest_asyncio
from yandex_music import Client

nest_asyncio.apply()

ym = Client().init()


api_id = "APT_ID"
api_hash = "API_HASH"
t_number = "PHONE"

client = TelegramClient('anon', api_id, api_hash,system_version="4.16.30-vxCUSTOM")

timer1 = 0

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}

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

        global timer1

        sleep_time = 15

        poloska = ""

        artist = await get_media_info()
        title = await get_media_info()
        print(f"Artist: {artist}, Song: {title}")
        user = await client.get_me()
        fullUser = await client(GetFullUserRequest(user))

        search_result = ym.search(f"{artist[0]} - {artist[1]}")

        text = [f'результат по запросу: {artist[0]} - {artist[1]}']
        best_result_text = ''

        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result
            text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

            if type_ in ['track', 'podcast_episode']:
                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(f'Содержимое лучшего результата: {best_result_text}\n')

        if search_result.artists:
            text.append(f'Исполнителей: {search_result.artists.total}')
        if search_result.albums:
            text.append(f'Альбомов: {search_result.albums.total}')
        if search_result.tracks:
            text.append(f'Треков: {search_result.tracks.total}')
        if search_result.playlists:
            text.append(f'Плейлистов: {search_result.playlists.total}')
        if search_result.videos:
            text.append(f'Видео: {search_result.videos.total}')

        text.append('')
        print('\n'.join(text))

        print(f"Время в милисекундах {best.duration_ms}")
        secs = best.duration_ms // 1000
        mins = secs // 60
        sec = secs - mins * 60
        print(f"secs={secs}; mins={mins},sec={sec}")
        print(f"Продолжительность трека: {mins}:{sec}")

        if(timer1<secs):
            if(secs-timer1<30):
                sleep_time = secs-timer1+7
                timer1=secs

            #if(secs-timer1<30):
             #   timer1 = timer1 + random.randint(5,8)
            else:
                timer1 =timer1 +  random.randint(13, 17)
            #if(timer1>=secs):
             #   timer1=0
            print(f"timer = {timer1}")
            #main()

        percent = (timer1/secs)*100
        print(f"percent is {percent}")

        if(percent <= 15):
            poloska = "●───────"
        elif(percent <= 40 and percent > 0):
            poloska = '──●─────'
        elif(percent <=60 and percent >30):
            poloska = '────●───'
        elif(percent <=90 and percent >60):
            poloska = '──────●─'
        elif(percent<=100 and percent>90):
            poloska = '───────●'

        if(timer1>=60):

            cur_min = timer1//60
            cur_sec = timer1 - cur_min*60
            print(f'curmin = {cur_min} cursed = {cur_sec}')
        else:
            cur_min = 0
            cur_sec = timer1
            print(f'cursec = {cur_sec}')

        try:
            async with client:
                if (cur_sec < 10 and sec < 10):
                    await client(UpdateProfileRequest(about=f"VK🎵|{artist[0]} - {artist[1]}| 0{cur_min}:0{cur_sec} {poloska} 0{mins}:0{sec}"))
                elif(sec<10):
                    await client(UpdateProfileRequest(about=f"VK🎵|{artist[0]} - {artist[1]}| 0{cur_min}:{cur_sec} {poloska} 0{mins}:0{sec}"))
                elif(cur_sec<10):
                    await client(UpdateProfileRequest(about=f"VK🎵|{artist[0]} - {artist[1]}| 0{cur_min}:0{cur_sec} {poloska} 0{mins}:{sec}"))
                else:
                    await client(UpdateProfileRequest(about=f"VK🎵|{artist[0]} - {artist[1]}| 0{cur_min}:{cur_sec} {poloska} 0{mins}:{sec}"))
        except Exception:
            async with client:
                await client(UpdateProfileRequest(about=f"VK🎵|None - None"))

        if fullUser.full_user.about:
            #pass
            print(user.first_name + " has the following Bio:")
            print(fullUser.full_user.about)

        if (secs - timer1 < 30):
            timer1 = 0

        await asyncio.sleep(sleep_time)

        async with client:
            client.loop.run_until_complete(main())

with client:
    client.loop.run_until_complete(main())

input('Press ENTER to exit')
