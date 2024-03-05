import logging
import random
import requests
import os
from bs4 import BeautifulSoup

from discord.ext import commands
from ..utils.commons import send_funny_fallback_msg


class BonerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="boner")
    async def fetch_boner_quote(self, ctx):
        base_url = "https://egzorcysta.fandom.com/wiki/Bogdan_Boner"
        try:
            response = requests.get(base_url)
            if response.status_code != 200:
                send_funny_fallback_msg(ctx)
                logging.error(f"Unable to access the website.")

            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = soup.find_all('li')
            selected_quote = random.choice(quotes).get_text()
            random_quote = selected_quote.split('(')[0].strip()

            counter = 0
            if len(random_quote) < 20 and counter <= 10:
                counter + 1
                await self.fetch_boner_quote(ctx)
            else:
                if random_quote:
                    await ctx.send(random_quote)
                else:
                    send_funny_fallback_msg(ctx)
                    logging.info(f"No Boner quotes available.")
        except Exception as e:
            await send_funny_fallback_msg(ctx)
            logging.error("Couldn't Boner quotes.")


async def setup(bot):
    await bot.add_cog(BonerCog(bot))
