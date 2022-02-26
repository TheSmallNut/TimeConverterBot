import discord
import timeConverter
import tokens
from discord.ext import commands

bot = discord.Client()
bot = commands.Bot(command_prefix="?")


@ bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@ bot.event
async def on_message(ctx):
    print(ctx.content)
    timeSaid = timeConverter.stringToDatetimeParser(ctx.content)
    if timeSaid != None:
        print(timeSaid)
        if "in" in ctx.content:
            print("in!")


bot.run(tokens.test)
