import os

from dotenv import load_dotenv
from __main__ import bot


async def send_funny_fallback_msg(ctx):
    load_dotenv(".env")
    helper_user = bot.get_user(int(os.getenv('target_user_id')))
    await ctx.send(f"{ctx.author.mention}, wybacz ale coś sie schrzaniło :/ {helper_user.mention} przyłaź tu i mnie napraw!")
