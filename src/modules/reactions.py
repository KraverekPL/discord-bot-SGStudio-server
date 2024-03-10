# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import os
import random

from discord.ext import commands

from ..services.open_ai import OpenAIService
from ..utils.commons import remove_polish_chars, load_resources_from_file


def load_keyword_responses():
    """Load keywords and responses from file."""
    main_dictionary = {}
    try:
        file = load_resources_from_file('keyword_responses.txt')
        for line in file:
            if ':' in line:
                keywords, responses = line.strip().split(':', 1)
                for single_keyword in keywords.split(','):
                    main_dictionary[single_keyword] = responses.strip().split('|')
            else:
                logging.warning(f"Invalid line format in the file: {line}")
    except Exception as e:
        logging.error(f"Exception e: {e}")
        return {}

    # Checking if dictionary is loaded properly
    if not main_dictionary:
        logging.warning("Empty or invalid keyword_responses dictionary.")
    for keyword, response in main_dictionary.items():
        if not isinstance(keyword, str) or not isinstance(response, list):
            logging.warning("Invalid format in keyword_responses.")
    for keyword, response in main_dictionary.items():
        if not response:
            logging.warning(f"Empty response for keyword: {keyword}.")
    logging.info(f"Loaded keyword_responses.txt")
    return main_dictionary


def load_responses_to_taunts():
    """Load responses to taunts from the specified file."""
    responses_to_taunts = []
    for line in load_resources_from_file('responses_to_taunts.txt'):
        responses_to_taunts.append(line)
    # Return the list of responses_to_taunts
    logging.info(f"Loaded file responses_to_taunts.txt")
    return responses_to_taunts


async def get_response_from_openai(enable_ai, message, open_ai_model):
    if enable_ai:
        open_ai_service = OpenAIService(open_ai_model)
        response_from_ai = open_ai_service.chat_with_gpt(message)
        if response_from_ai is not None:
            await message.channel.send(response_from_ai)
            logging.info(f"Response from OpenAi with msg: {message.content.strip()}:{response_from_ai}")
        else:
            await message.channel.send('Nie wiem :(')
            logging.info(f"message was too long. Skipping API call.")
    else:
        await message.channel.send('Nie wiem :(')
        logging.info(f"OpenAi API is turned off. Sending default message.")


class ReactionCog(commands.Cog):
    DISABLE_REACTIONS = False

    def __init__(self, bot):
        self.bot = bot
        self.keyword_responses = load_keyword_responses()
        self.responses_to_taunts = load_responses_to_taunts()

    # Enable reactions after X time
    async def delayed_reaction_enable(self, sleep_time):
        await asyncio.sleep(int(sleep_time))
        self.DISABLE_REACTIONS = False
        logging.info(f"ReactionCog is enabled again. Status: {self.get_bot_reaction_status()}")

    def get_bot_reaction_status(self):
        return "disabled" if self.DISABLE_REACTIONS else "enabled"

    async def disable_reactions_if_asked(self, message):
        sleep_time = os.getenv('bot_silent_time')
        if self.bot.user.mentioned_in(message):
            # Toggle reactions on/off.
            spam_hooks = ['morda', 'mordę', 'morde']
            for word in spam_hooks:
                if word in message.content.lower():
                    self.DISABLE_REACTIONS = not self.DISABLE_REACTIONS
                    logging.info(
                        f"ReactionCog will be disabled for {sleep_time}. Status: {self.get_bot_reaction_status()}")
                    await message.channel.send(f"Przepraszam za spam. Wyłączam moduł rekacji na 15 minut.")
                    await asyncio.create_task(self.delayed_reaction_enable(900))
                    return True
        return False

    async def get_taunt_response_from_bot(self, message):
        if self.bot.user.mentioned_in(message):
            config_data = load_resources_from_file('bot_scary_responses.json')
            list_of_words = config_data.get("list_of_words", [])
            list_of_responses = config_data.get("list_of_responses", [])

            for word in list_of_words:
                # Check for words in the list, removing Polish characters in-fly
                normalized_message = remove_polish_chars(message.content.lower())
                if word in normalized_message:
                    rng_response_for_scary_taunt = random.choice(list_of_responses)
                    await message.channel.send(rng_response_for_scary_taunt)
                    logging.info(f"Response for scary taunt a bot with {word}:{rng_response_for_scary_taunt}")
                    return True
        return False

    async def get_reaction_for_random_message(self, message):
        if not self.bot.user.mentioned_in(message):
            for keyword, response in self.keyword_responses.items():
                if keyword.lower() in message.content.lower():
                    # Send a random response if the random condition is met
                    magic_random = random.random()
                    is_on_bot_channel = message.channel.id == 1214161316177125376  # ID of 'bot_channel'
                    if (is_on_bot_channel and magic_random < 0.4) or (not is_on_bot_channel and magic_random < 0.2):
                        random_response = random.choice(response)
                        logging.info(
                            f"Keyword response for {message.author} on_message: {keyword.lower()}:{random_response}. "
                            f"random.random():{magic_random}")
                        await message.channel.send(content=random_response)
                        return True
                    else:
                        logging.info(f"No response - random.random():{magic_random} decided :)")
                        return True
        return False

    async def get_reaction_when_bot_is_mentioned(self, message):
        if self.bot.user.mentioned_in(message):
            enable_ai = os.getenv("enabled_ai", 'False').lower() in ('true', '1', 't')
            open_ai_model = os.getenv('open_ai_model')
            if message.content.strip() == f'<@{self.bot.user.id}>':
                # If the message is empty and the bot is not mentioned - send friendly wake up
                await self.send_friendly_awake(message)
                return True
            else:
                # If the message has content and the bot is mentioned - send it to Open API gateway
                await get_response_from_openai(enable_ai, message, open_ai_model)
                return True
        return False

    async def send_friendly_awake(self, message):
        rng_response_for_friendly_taunt = random.choice(self.responses_to_taunts)
        await message.channel.send(rng_response_for_friendly_taunt)
        logging.info(
            f"Response for call friendly bot with {message.content.strip()}:{rng_response_for_friendly_taunt}")

    @commands.command(name='pobudka')
    async def wake_up_bot(self, ctx):
        """Command to wake up the bot by administrators."""
        allowed_user_ids = {os.getenv('target_user_id')}
        if ctx.author.guild_permissions.administrator or ctx.author.id in allowed_user_ids:
            self.DISABLE_REACTIONS = False
            logging.info(f"ReactionCog is enabled again. Status: {self.get_bot_reaction_status()}")
            await ctx.send("Bot został wybudzony!")
        else:
            helper_user = self.bot.get_user(267243681021427713)
            await ctx.send(f"Nie masz uprawnień do tej komendy! Tylko {helper_user.mention} może wykonać ta komende.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Event handler called when a message is received."""
        # Ignore messages from bot
        if message.author.bot:
            return
        # Disable all response from bot
        if self.DISABLE_REACTIONS:
            logging.info(
                f"ReactionCog is silent for message: {message.content}. Status: {self.get_bot_reaction_status()}")
            return

        # Disable reactions for period of time if asked by user
        if await self.disable_reactions_if_asked(message):
            return

        # Check for responses to taunts bot when the bot is mentioned to be silent
        if await self.get_taunt_response_from_bot(message):
            return

        # If a bot is mentioned, it will say hello or answer your question depending on the content of the message
        if await self.get_reaction_when_bot_is_mentioned(message):
            return

        # Check for keyword and respond with proper response from file if keyword exist
        if await self.get_reaction_for_random_message(message):
            return


async def setup(bot):
    await bot.add_cog(ReactionCog(bot))
