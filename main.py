# -*- coding: utf-8 -*-
import logging
import asyncio
import os
import random

import discord

from dotenv import load_dotenv
from discord.ext import commands

# Logging configuration
load_dotenv(".env")
logging.basicConfig(level=os.getenv('log_level'), format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info('---------------------------------------------------------------')
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    logging.info(f'Loading cogs:')

    do_not_load_those_cogs = ['__init__']
    # Loading cogs from the "modules" folder
    for filename in os.listdir('src/modules'):
        if filename.endswith('.py') and filename[:-3] not in do_not_load_those_cogs:
            try:
                await bot.load_extension(f'src.modules.{filename[:-3]}')
                logging.info(f'Loaded cog: {filename[:-3]}')
            except commands.ExtensionError as e:
                logging.error(f'Error loading cog {filename[:-3]}: {e}')

    # Adding bot status
    await zmien_status()

    logging.info(f'All cogs successfully loaded!')
    logging.info(f'Log level: ' + os.getenv('log_level'))
    logging.info(f'Bot silent time: ' + os.getenv('bot_silent_time'))
    logging.info(f'Enable AI (OpenAI): ' + os.getenv('enabled_ai'))
    logging.info('---------------------------------------------------------------')
    await cleanup_temp_music()


async def zmien_status():
    while True:
        with open('src/resources/bot_statuses.txt', 'r', encoding='utf-8') as file:
            for line in file:
                status = random.choice(line.split(','))
                await bot.change_presence(status=str(status))
                await asyncio.sleep(300)  # change status every 5 mins


async def cleanup_temp_music():
    folder_path = 'temp_music'  # Ustaw odpowiednią ścieżkę do folderu
    try:
        # Usuń wszystkie pliki w folderze temp_music
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Deleting file: {file_path}")
    except Exception as e:
        logging.error(f'Exception during cleaning "temp_music": {e}')


async def main():
    try:
        await bot.start(os.getenv("BOT_TOKEN"))
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
