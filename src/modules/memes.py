import discord
import logging
import requests
from bs4 import BeautifulSoup
import re
import time

from discord.ext import commands
from ..utils.commons import send_funny_fallback_msg


class MemesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mem")
    async def fetch_mem(self, ctx):
        max_retries = 5
        for _ in range(max_retries):
            try:
                response = requests.get("https://jbzd.com.pl/losowe")
                soup = BeautifulSoup(response.content, 'html.parser')

                pattern = re.compile(r'https://i1\.jbzd\.com\.pl/contents/\d{4}/\d{2}/[a-zA-Z0-9]+\.(jpg|gif|png|mp4)')
                meme_element = soup.find(
                    lambda tag: tag.name in ['img', 'video'] and 'src' in tag.attrs and pattern.match(tag['src']))
                meme_url = meme_element['src'] if meme_element else None
                logging.info(f"Loading meme from: {meme_url}")

                title_element = soup.find('meta', {'property': 'og:title'})
                title = title_element['content'] if title_element else "Losowy Memik"

                if meme_url:
                    embed = discord.Embed(title=title)
                    if meme_url.endswith('.mp4'):
                        embed.add_field(name="Meme", value=meme_url)
                    else:
                        embed.set_image(url=meme_url)
                    await ctx.send(embed=embed)
                    return

            except Exception as e:
                await send_funny_fallback_msg(ctx)
                logging.error("Couldn't fetch a meme.")

            time.sleep(1)

        # If no meme is found after all retries
        await send_funny_fallback_msg(ctx)


async def setup(bot):
    await bot.add_cog(MemesCog(bot))
