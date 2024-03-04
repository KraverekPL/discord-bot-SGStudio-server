# -*- coding: utf-8 -*-
import logging
import os
import random

from discord.ext import commands


class ReactionCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.keyword_responses = self.load_keyword_responses()

    def load_keyword_responses(self):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        """Event handler called when a message is received."""
        if message.author.bot:
            return
        for keyword, response in self.keyword_responses.items():
            if keyword.lower() in message.content.lower():
                if random.random() < 0.6:
                    random_response = random.choice(response)
                    logging.info(
                        f"Keyword response for {message.author} on_message: {keyword.lower()}:{random_response}")
                    await message.channel.send(content=random_response)
                else:
                    logging.info(f"No response - random.random() decided :)")


async def setup(bot):
    await bot.add_cog(ReactionCog(bot))
