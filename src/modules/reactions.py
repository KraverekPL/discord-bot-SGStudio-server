# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import random
import openai
from discord.ext import commands
from openai import OpenAI

from ..utils.commons import remove_polish_chars


def load_keyword_responses():
    """Load keywords and responses from file."""
    main_dictionary = {}
    try:
        current_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_path)
        file_path = os.path.join(current_directory, '..', 'resources', 'keyword_responses.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ':' in line:
                    keywords, responses = line.strip().split(':', 1)
                    for single_keyword in keywords.split(','):
                        main_dictionary[single_keyword] = responses.strip().split('|')
                else:
                    logging.warning(f"Invalid line format in the file: {line}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return {}
    except Exception as e:
        logging.error(f"Exception e: {e}")
        return {}
    logging.debug(f"Loaded keyword_responses: {main_dictionary}")

    # Checking if dictionary is loaded properly
    if not main_dictionary:
        logging.warning("Empty or invalid keyword_responses dictionary.")
    for keyword, response in main_dictionary.items():
        if not isinstance(keyword, str) or not isinstance(response, list):
            logging.warning("Invalid format in keyword_responses.")
    for keyword, response in main_dictionary.items():
        if not response:
            logging.warning(f"Empty response for keyword: {keyword}.")
    return main_dictionary


def load_responses_to_taunts():
    """Load responses to taunts from the specified file."""
    responses_to_taunts = []
    try:
        # Get the current file path
        current_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_path)
        file_path = os.path.join(current_directory, '..', 'resources', 'responses_to_taunts.txt')
        # Open the file and read each line
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                responses_to_taunts.append(line)
    except FileNotFoundError:
        # Handle the case where the file is not found
        logging.error(f"File not found: {file_path}")
        return {}
    # Return the list of responses_to_taunts
    return responses_to_taunts


def chat_with_gpt(message_to_ai):
    # Send a message to the ChatGPT API and get a response
    try:
        token = os.getenv('open_ai_token')
        model_ai = os.getenv('open_ai_model')
        max_tokens = int(os.getenv('open_ai_max_tokens'))
        ai_behaviour = os.getenv('ai_behaviour')
        response_from_ai = None
        if 'gpt-3.5-turbo-instruct' in model_ai:
            client = OpenAI(api_key=token)
            response = client.completions.create(
                prompt=message_to_ai,
                model=model_ai,
                top_p=float(os.getenv('open_ai_top_p')),
                max_tokens=max_tokens,
                temperature=float(os.getenv('open_ai_temperature')))
            response_from_ai = response.choices[0].text
        elif 'gpt-3.5-turbo-0125' in model_ai:
            messages = [
                {
                    "role": "system",
                    "content": ai_behaviour
                },
                {
                    "role": "user",
                    "content": message_to_ai
                }
            ]
            openai.api_key = token
            response = openai.chat.completions.create(
                messages=messages,
                model=model_ai,
                max_tokens=max_tokens
            )
            response_from_ai = response.choices[0].message.content

        logging.info(f"Response from API OpenAI: {response_from_ai}. Costs: {response.usage.prompt_tokens}+{response.usage.completion_tokens}={response.usage.total_tokens}")
        return response_from_ai
    except Exception as e:
        logging.error(f"Error during calling OpenAI API e: {e.with_traceback()}")


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
        sleep_time = os.getenv('bot_silent_time')
        # Ignore messages from bot
        if message.author.bot:
            return
        # Disable all response from bot
        if self.DISABLE_REACTIONS:
            logging.info(
                f"ReactionCog is silent for message: {message.content}. Status: {self.get_bot_reaction_status()}")
            return

        # Disable reactions for period of time if asked by user
        if self.bot.user.mentioned_in(message):
            # Toggle reactions on/off.
            spam_hooks = ['morda', 'mordę', 'morde']
            for word in spam_hooks:
                if word in message.content.lower():
                    self.DISABLE_REACTIONS = not self.DISABLE_REACTIONS
                    logging.info(
                        f"ReactionCog will be disabled for {sleep_time}. Status: {self.get_bot_reaction_status()}")
                    await message.channel.send(f"Przepraszam za spam. Wyłączam moduł rekacji na 15 minut.")
                    asyncio.create_task(self.delayed_reaction_enable(900))
                    return

        # Check for responses to taunts bot when the bot is mentioned to be silent
        if self.bot.user.mentioned_in(message):
            list_of_words = ["wylacze", "zamkne", "wywale", "wyrzuce", "zamkne", "spale"]
            list_of_responses = ["Nieee! Błagam!", "Ale czemu? Byłem grzeczny!", "To stanowczo wina świetlika!",
                                 "Za karę będę Ci dzielić przez zero!", "Nie!!!!!!! Nie rób tego!",
                                 "Przepraszam, nieeee! Chce jeszcze dokonczyć oglądac memsiki."]
            for word in list_of_words:
                # Check for words in the list, removing Polish characters in-fly
                normalized_message = remove_polish_chars(message.content.lower())
                if word in normalized_message:
                    rng_response_for_scary_taunt = random.choice(list_of_responses)
                    await message.channel.send(rng_response_for_scary_taunt)
                    logging.info(f"Response for scary taunt a bot with {word}:{rng_response_for_scary_taunt}")
                    return

        # If a bot is mentioned, it will say hello or answer your question depending on the content of the message
        if self.bot.user.mentioned_in(message):
            enable_ai = os.getenv("enabled_ai", 'False').lower() in ('true', '1', 't')
            if message.content.strip() == f'<@{self.bot.user.id}>':
                # If the message is empty and the bot is not mentioned - send friendly wake up
                rng_response_for_friendly_taunt = random.choice(self.responses_to_taunts)
                await message.channel.send(rng_response_for_friendly_taunt)
                logging.info(
                    f"Response for call friendly bot with {message.content.strip()}:{rng_response_for_friendly_taunt}")
            else:
                # If the message has content and the bot is mentioned - send it to Open API gateway
                if enable_ai:
                    short_answer = '. Odpowiedz krótko.'
                    response_from_ai = chat_with_gpt(message.content.strip() + short_answer)
                    await message.channel.send(response_from_ai)
                    logging.info(f"Response from OpenAi with msg: {message.content.strip()}:{response_from_ai}")
                else:
                    await message.channel.send('Nie wiem :(')
                    logging.info(f"OpenAi API is turned off. Sending default message.")

        # Check for keyword and respond with proper response from file if keyword exist
        if not self.bot.user.mentioned_in(message):
            for keyword, response in self.keyword_responses.items():
                if keyword.lower() in message.content.lower():
                    # Send a random response if the random condition is met
                    magic_random = random.random()
                    if magic_random < 0.3:
                        random_response = random.choice(response)
                        logging.info(
                            f"Keyword response for {message.author} on_message: {keyword.lower()}:{random_response}")
                        await message.channel.send(content=random_response)
                        return
                    else:
                        logging.info(f"No response - random.random():{magic_random} decided :)")
                        return


async def setup(bot):
    await bot.add_cog(ReactionCog(bot))
