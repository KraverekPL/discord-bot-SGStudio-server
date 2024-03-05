import discord

from discord.ext import commands


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pomoc', aliases=['commands'])
    async def show_help_global(self, ctx):
        """Show all available commands."""
        embed = discord.Embed(title="Komendy Bota", description="Mały pomocnik bota – komendy w skrócie. Humor w każdej chwili - bot, który zawsze dostarcza rozrywki.",  color=0xC4741D)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1214162287259025428/bc40ba46841471b5f49d3bf7d569ce58.webp?size=80")
        embed.add_field(name="!joke", value="Opowiada żart. Pobiera go z repozytorium 4500 żartów", inline=False)
        embed.add_field(name="!mem", value="Wyświetla losowego mema z jbzd.pl", inline=False)
        embed.add_field(name="@Mały Warchlak", value="Budzi bota. Bot wesoło reaguje.", inline=False)
        embed.add_field(name="morda", value="Straszy bota. Wyłącza reakcje na 15 minut. Trzeba napisać mu to jako odpowiedź na jego post.", inline=False)
        source_code_link = "https://github.com/KraverekPL/discord-bot-SGStudio-server"
        embed.add_field(name='\u200B', value=f"Źródło kodu: [link]({source_code_link})", inline=False)
        footer_text = f"Bot stworzony przez przez Kraverek"
        embed.set_footer(text=footer_text)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
