import logging
import random

from discord.ext import commands


class AdminToolsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def wake_up(self):
        logging.info("Waking up the bot bot!")

    @commands.command(name='mapuj', )
    async def show_help_global(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Add a reaction to a user's message
        if message.author.id == 725426177790967818:
            try:
                custom_reactions = [
                    "💩", "👍", "❤️", "🎉", "🤔", "🔥", "🚀", "🌈", "🍕", "🎮",
                    "🌟", "🎸", "🐱", "🌺", "🍦", "📚", "🎭", "🍣", "🏆", "💯",
                    "😂", "😍", "🤣", "😎", "😇", "😜", "😊", "🙌", "👏", "🍀",
                    "🥳", "🤗", "🎊", "🎈", "👻", "🍩", "🍭", "🎁", "🍺", "🍸"
                ]
                await message.add_reaction(random.choice(custom_reactions))
                logging.info(f"Add reactions to 725426177790967818 user.")
            except Exception as e:
                logging.error(f"Error adding reaction: {e}")







async def setup(bot):
    await bot.add_cog(AdminToolsCog(bot))
