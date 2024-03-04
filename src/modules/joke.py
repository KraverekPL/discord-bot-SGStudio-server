import logging
import random
import requests
import os
from bs4 import BeautifulSoup

from discord.ext import commands
from ..utils.commons import send_funny_fallback_msg


class JokesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def fetch_joke(self, ctx):
        page_number = random.randint(2, 350)
        base_url = 'https://perelki.net/?ps='
        try:
            await ctx.send(f"To słuchaj tego {ctx.author.mention}!")
            response = requests.get(base_url + str(page_number))
            if response.status_code != 200:
                await send_funny_fallback_msg(ctx)
                logging.error(f"Couldn't fetch a joke. Status code of request: {response.status_code}")

            soup = BeautifulSoup(response.content, 'html.parser')
            jokes = soup.find_all("div", class_="container joke-here")

            if jokes:
                random_joke = random.choice(jokes)
                # Removing "about" elements
                for about_div in random_joke.find_all("div", class_="about"):
                    about_div.decompose()

                # Adding new lines after list items and colons
                joke_text = ''.join(random_joke.stripped_strings).replace('-', '\n-')
                logging.info(f"Joke: {joke_text}")
                await ctx.send(joke_text)
            else:
                await send_funny_fallback_msg(ctx)
                logging.error("Couldn't fetch a joke.")

        except Exception as e:
            await send_funny_fallback_msg(ctx)
            logging.error(f"Couldn't fetch a joke. Exception in joke method e: {e} ")


async def setup(bot):
    await bot.add_cog(JokesCog(bot))
