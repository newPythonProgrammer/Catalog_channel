import pyrogram
import config
import requests
import json
import asyncio
import aiohttp
from bot import client_pyrogram


# client_pyrogram = pyrogram.Client("my_account", config.API_ID_ACC, config.API_HASH_ACC)
# client_pyrogram.start()


headers = {
    'Authorization':'Bearer aibPlLZp9xBECPmowrbFtw9WF0OY92ZFHwsGEXgIqWxf8x2y97WB40xtOtMSBF7KaGA3DaQeoxq8n'
}

async def get_name_chanel(link):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)

        json_data = json.loads(await response.text())
        if json_data['status'] == 'ok':
            return json_data['response']['title']
        else:
            for i in range(10):
                response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)
                json_data = json.loads(await response.text())
                if json_data['status'] == 'ok':
                    return json_data['response']['title']
            return '***'


async def get_sub(link):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)
        json_data = json.loads(await response.text())
        if json_data['status'] == 'ok':
            return json_data['response']['participants_count']
        else:
            for i in range(10):
                response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)
                json_data = json.loads(await response.text())
                if json_data['status'] == 'ok':
                    return json_data['response']['participants_count']
            return '***'

async def get_views(link):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)
        json_data = json.loads(await response.text())
        if json_data['status'] == 'ok':
            return json_data['response']['avg_post_reach']
        else:
            for i in range(10):
                response = await session.get(f'https://api.telemetr.me/channels/stat?channelId={link}', headers=headers)
                json_data = json.loads(await response.text())
                if json_data['status'] == 'ok':
                    return json_data['response']['avg_post_reach']
            return '***'


async def get_photo_stat_and_sub(chanel_id, link):
    msg = await client_pyrogram.send_message(chat_id='telemetrmebot', text=link)
    await asyncio.sleep(10)
    message_photo = await client_pyrogram.get_messages(chat_id='telemetrmebot', message_ids=msg.id+1)
    if message_photo.caption is None:
        return None
    try:
        await client_pyrogram.download_media(message_photo, file_name=f'img/stat_{chanel_id}.jpg')
    except:
        pass
    message_stat = await client_pyrogram.get_messages(chat_id='telemetrmebot', message_ids=msg.id+2)
    text = message_stat.text.split('\n', maxsplit=1)
    return text[1]


