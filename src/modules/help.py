import logging
import random
import requests
import os
from bs4 import BeautifulSoup

from discord.ext import commands
from ..utils.commons import send_funny_fallback_msg


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def show_help(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
