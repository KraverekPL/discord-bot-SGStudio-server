# -*- coding: utf-8 -*-
import logging
import asyncio
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

# Logging configuration
logging.basicConfig(level='INFO', format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id}) \n -------------')

    # Loading cogs from the "modules" folder
    for filename in os.listdir('src/modules'):
        if filename.endswith('.py') and not filename.startswith('__init__'):
            try:
                await bot.load_extension(f'src.modules.{filename[:-3]}')
                logging.info(f'Loaded cog: {filename[:-3]}')
            except commands.ExtensionError as e:
                logging.error(f'Error loading cog {filename[:-3]}: {e}')


async def main():
    try:
        load_dotenv(".env")
        await bot.start(os.getenv("BOT_TOKEN"))
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
