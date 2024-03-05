import os
import unicodedata
import logging

from dotenv import load_dotenv
from __main__ import bot


async def send_funny_fallback_msg(ctx):
    load_dotenv(".env")
    helper_user = bot.get_user(int(os.getenv('target_user_id')))
    await ctx.send(
        f"{ctx.author.mention}, wybacz ale coś sie schrzaniło :/ {helper_user.mention} przyłaź tu i mnie napraw!")


def remove_polish_chars(text):
    mapping = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }

    return ''.join(mapping.get(char, char) for char in text)
