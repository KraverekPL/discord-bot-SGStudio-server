import logging
import random
import requests
import os
from bs4 import BeautifulSoup

from discord.ext import commands
from ..utils.commons import send_funny_fallback_msg


class BombaCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bomba")
    async def fetch_bomba_quote(self, ctx):
        base_url = "https://nonsa.pl/wiki/Cytaty:Kapitan_Bomba"
        try:
            response = requests.get(base_url)
            if response.status_code != 200:
                send_funny_fallback_msg(ctx)
                logging.error(f"Unable to access the website.")

            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = []

            list_items = soup.find_all('li')
            for li in list_items:
                italics = li.find('i')
                if italics:
                    quotes.append('\n'.join(italics.stripped_strings))
                    random_quote = random.choice(quotes)
                    logging.info(f"Fetched Bomba quotes: {random_quote}.")

            if random_quote:
                await ctx.send(random_quote)
            else:
                send_funny_fallback_msg(ctx)
                logging.info(f"No Bomba quotes available.")
        except Exception as e:
            await send_funny_fallback_msg(ctx)
            logging.error("Couldn't fetch a Bomba quotes.")


async def setup(bot):
    await bot.add_cog(BombaCog(bot))
