import logging
import os

import discord
import random
from collections import Counter
from datetime import datetime
from discord.ext import commands


async def add_recationto_msg(message, user_id):
    # Add a reaction to a user's message
    if message.author.id == user_id:
        try:
            custom_reactions = [
                "💩", "👍", "❤️", "🎉", "🤔", "🔥", "🚀", "🌈", "🍕", "🎮",
                "🌟", "🎸", "🐱", "🌺", "🍦", "📚", "🎭", "🍣", "🏆", "💯",
                "😂", "😍", "🤣", "😎", "😇", "😜", "😊", "🙌", "👏", "🍀",
                "🥳", "🤗", "🎊", "🎈", "👻", "🍩", "🍭", "🎁", "🍺", "🍸"
            ]
            await message.add_reaction(random.choice(custom_reactions))
            logging.info(f"Add reactions to {message.author.id} user.")
        except Exception as e:
            logging.error(f"Error adding reaction: {e.with_traceback()}")


class AdminToolsCog(commands.Cog):

    ignore_words = ['alrik3287:', 'mack_m:', 'kraverek:', 'gregu:', 'dziobak37:', 'siara89:', 'czarna5664:',
                    "sunniva85:", 'retzelas:', 'gregu_:']

    def __init__(self, bot):
        self.bot = bot

    async def wake_up(self):
        logging.info("Waking up the bot bot!")

    @commands.command(name='mapuj', )
    async def make_backup(self, ctx, channel_id):
        try:
            # Retrieve a channel object based on its ID
            # Specify the IDs of the channels you want to collect messages from
            channel_ids = [989977861282734223, 1019239220000346172, 1019230294747926578, 1022506515199950929]
            if channel_id:
                channel_ids = [channel_id]
            allowed_user_ids = {int(os.getenv('target_user_id'))}
            all_messages = []
            if ctx.author.id in allowed_user_ids:
                for channel_id in channel_ids:
                    # Retrieve a channel object based on its ID
                    channel = self.bot.get_channel(channel_id)
                    if not channel:
                        logging.info(f"Cannot find channel with ID: {channel_id}")
                        continue
                    messages = []
                    async for message in channel.history(limit=None):
                        messages.append(message)
                    all_messages.extend(
                        [message.content if isinstance(message.content, str) else str(message.content) for message in
                         messages if isinstance(message, discord.Message)])
                    message_count_channel = len(messages)
                    logging.info(f"Channel history added to all all_messages container: {channel_id}, number of "
                                 f"messages: {message_count_channel}")

                message_count = len(all_messages)
                logging.info(f"Number of messages on channel ({channel_ids}): {message_count}.")

                # Save messages to a text file
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"backup_channels_{current_datetime}.txt"
                with open(file_name, "w", encoding="utf-8") as file:
                    for message in all_messages:
                        file.write(f"{message}\n")
                    logging.info(f"Backup completed. Messages from channel {channel_ids} saved to file {file_name}.")

                # Combine all messages into a single string
                all_text = ' '.join(all_messages)
                words_count = Counter(
                    word.lower() for word in all_text.split() if len(word) >= 5 and word not in self.ignore_words)

                # Display the top 10 most common words
                top_words = words_count.most_common(30)
                await ctx.send(f"Top 30 most common words: {top_words}")
                logging.info(f"Top 30 most common words: {top_words}")
            else:
                await ctx.send(f"Nie masz uprawnień do tej komendy!")
        except Exception as e:
            logging.info(f"An error occurred while backing up: {e.with_traceback()}")

    @commands.command(name='find')
    async def find_most_popular(self, ctx, file_name: str, number: int):
        try:
            messages = []
            allowed_user_ids = {os.getenv('target_user_id')}
            if ctx.author.id in allowed_user_ids:
                with open(file_name, 'r', encoding='utf-8') as file:
                    messages = file.readlines()
                # Combine all messages into a single string
                all_text = ' '.join(messages)
                # Split the text into words and count occurrences
                words_count = Counter(
                    word.lower() for word in all_text.split() if len(word) >= 5 and word not in self.ignore_words)
                # Display the top X most common words
                top_words = words_count.most_common(number)
                await ctx.send(f"Top {number} most common words: {top_words}")
                logging.info(f"Top {number} most common words: {top_words}")
            else:
                await ctx.send(f"Nie masz uprawnień do tej komendy!")
        except Exception as e:
            logging.info(f"An error occurred while backing up: {e.with_traceback()}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await add_recationto_msg(message, 725426177790967818)


async def setup(bot):
    await bot.add_cog(AdminToolsCog(bot))
