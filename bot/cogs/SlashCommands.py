import discord
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Say hello to the bot')
    async def hello(self, ctx):
        await ctx.respond("Hello! I am your Discord bot.")

    @discord.slash_command(description='Check the bot\'s latency')
    async def ping(self, ctx):
        await ctx.respond(f"Pong! Latency is {self.bot.latency}")

def setup(bot):
    bot.add_cog(SlashCommands(bot))