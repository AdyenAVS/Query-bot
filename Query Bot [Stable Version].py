import requests
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor
import asyncio

bot_token = '6529520308:AAGvZHvafWZu1zX-KBb3jhtnBBBsF-bYtyc'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    start_time = time.time()  # Tiempo de inicio del comando
    ping_message = await message.reply("Bot Online ⓘ")
    end_time = time.time()  # Tiempo de finalización del comando

    response_time = end_time - start_time  # Calcula el tiempo de respuesta

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=ping_message.message_id,
        text=f"Bot Online ⓘ\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 𝘁𝗶𝗺𝗲: {response_time:.2f} seconds"
    )

def get_main_url(url):
    return urlparse(url).netloc

def get_urls(keyword, num_results):
    urls = []
    page = 1
    while len(urls) < num_results:
        url = f"https://www.google.com/search?q={keyword}&start={page*10}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('a', href=True)
        for link in results:
            url = link['href']
            if url.startswith('/url?q='):
                url = url[7:].split('&')[0]
                if 'google' not in url and url not in urls:
                    urls.append(url)
                    if len(urls) == num_results:
                        return urls
        page += 1
        time.sleep(1)  
    return urls

@dp.message_handler(commands=['ht'])
async def analyze_command(message: types.Message):
    args = message.get_args().split('|')
    if len(args) < 2:
        await message.reply("𝗨𝘀𝗮𝗴𝗲: /ht [𝗞𝗲𝘆𝘄𝗼𝗿𝗱𝘀] | [𝗡𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝗿𝗲𝘀𝘂𝗹𝘁𝘀]")
        return

    keyword = args[0]
    num_results = int(args[1].strip())
    dork_used = f"𝗗𝗼𝗿𝗸 𝘂𝘀𝗲𝗱: {keyword}"

    loading_message = await message.reply("\n━━━━━━━━━━━━━\n𝐒𝐭𝐚𝐭𝐮𝐬: 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠...\n━━━━━━━━━━━━━")

    urls = get_urls(keyword, num_results)
    result_message = f"𝗥𝗲𝘀𝘂𝗹𝘁𝘀 𝗳𝗼𝘂𝗻𝗱\n━━━━━━━━━━━━━\n{dork_used}\n━━━━━━━━━━━━━"
    for url in urls:
        result_message += f"\n[き] 𝗦𝗶𝘁𝗲: {url}"

    await bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text=result_message, parse_mode=types.ParseMode.MARKDOWN)


    for i in range(3):  
        dots = '■■■■' * (i + 1)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text=f"\n━━━━━━━━━━━━━\n𝐒𝐭𝐚𝐭𝐮𝐬: 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠...\n{dots}\n━━━━━━━━━━━━━")
        await asyncio.sleep(1)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text=result_message)

if __name__ == '__main__':
    executor.start_polling(dp)
 