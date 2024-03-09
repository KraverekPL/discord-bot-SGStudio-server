# -*- coding: utf-8 -*-
import logging
import asyncio
import os
import random
import json
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks

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
                logging.error(f'Error loading cog {filename[:-3]}: {e.with_traceback()}')

    logging.info(f'All cogs successfully loaded!')
    logging.info(f'Log level: ' + os.getenv('log_level'))
    logging.info(f'Bot silent time: ' + os.getenv('bot_silent_time'))
    logging.info(f'Enable AI (OpenAI): ' + os.getenv('enabled_ai'))
    logging.info('---------------------------------------------------------------')
    await cleanup_temp_music()
    # Adding bot status
    change_status.start()


@tasks.loop(minutes=15)
async def change_status():
    activity_type, status_list = choose_activity()
    if status_list:
        status = random.choice(status_list)
        activity = discord.Game(name=status) if activity_type == discord.ActivityType.playing else discord.Activity(
            type=activity_type, name=status)
        await bot.change_presence(activity=activity)
        logging.info(f"Bot's current activity set to: {status} - Type: {activity_type}")


def choose_activity():
    try:
        with open('src/resources/bot_activities.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        activity_type = random.choice(['playing', 'listening'])
        status_list = data.get(activity_type, [])

        return (discord.ActivityType.playing, status_list) if activity_type == 'playing' else (
            discord.ActivityType.listening, status_list)

    except FileNotFoundError:
        logging.error("Error: File 'bot_activities.json' not found.")
        return discord.ActivityType.playing, []


def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []


async def cleanup_temp_music():
    folder_path = 'temp_music'
    try:
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
