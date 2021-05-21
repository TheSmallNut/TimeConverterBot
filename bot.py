import discord
import json
import tokens
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dateutil import parser, tz
from datetime import datetime, timezone
import pytz
from pytz import timezone


def openJsonDoc(nameOfDoc="settings"):
    with open(f'{str(nameOfDoc)}.json', 'r') as f:
        data = json.load(f)
    return data


settings = openJsonDoc()


def getGuildIndex(guild):
    for i in range(len(settings["guilds"])):
        if settings["guilds"][i]["id"] == guild.id:
            return int(i)
    return -1


def writeJsonDoc(dumpData=settings, location="settings"):
    with open(f'{location}.json', 'w') as f:
        json.dump(dumpData, f, indent=4)


def get_prefix(client, message):
    return settings["guilds"][getGuildIndex(message.guild)]["prefix"]


def stringToDate(string):
    date = parser.parse(
        string, fuzzy=True)
    return date


bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix)


async def sendEmbedMessage(channel, Title, Description, Color=0x586A8E):
    embedVar = discord.Embed(title=Title, description=Description, color=Color)
    await channel.send(embed=embedVar)


@ bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@ bot.event
async def on_guild_join(guild):
    settings["guilds"].append({})
    location = settings["guilds"][-1]
    location["id"] = guild.id
    location["name"] = guild.name
    location["prefix"] = "$"
    location["region"] = guild.region
    location["timeZones"] = []
    location["defaultTimeZone"] = "UTC"
    writeJsonDoc()


@ bot.event
async def on_message(ctx):
    print(ctx.content)
    try:
        date = stringToDate(ctx.content)
        guildLocation = settings["guilds"][getGuildIndex(ctx.guild)]
        if date.tzinfo == None:
            date = date.replace(tzinfo=timezone(
                guildLocation["defaultTimeZone"]))
        description = ""
        embed = discord.Embed(
            title=f"Times from {date.tzinfo}", color=0x586A8E)
        for TIMEZONE in guildLocation["timeZones"]:
            to_zone = tz.gettz(TIMEZONE)
            f = '{0:>1}:{1:>2} | {2} \n'
            convertedTime = date.astimezone(to_zone)
            # description += f"{convertedTime.hour}:{convertedTime.minute} | {TIMEZONE} \n"
            embed.add_field(
                name=TIMEZONE, value=f"{convertedTime.hour}:{convertedTime.minute}")
        # await sendEmbedMessage(ctx.channel, f"Times from {date.tzinfo}", description)
        await ctx.channel.send(embed=embed)
    except parser._parser.ParserError:
        pass
    await bot.process_commands(ctx)


@ bot.command(name="addTimezone", aliases=["at", "AT", "aT", "ADDTIMEZONE", "addtimezone", "AddTimezone"])
@ has_permissions(manage_messages=True)
async def _addTimezone(ctx, timezone):
    if timezone not in pytz.all_timezones:
        print("NOT A TIMEZONE")
        return
    timeZones = settings["guilds"][getGuildIndex(ctx.guild)]["timeZones"]
    if timezone in timeZones:
        print("This is already a timezone")
        return
    timeZones.append(timezone)
    writeJsonDoc()
    print(f"Added timezone : {timezone}")


@ bot.command(name="removeTimezone", aliases=["rt", "RT", "rT", "REMOVETIMEZONE", "removetimezone", "RemoveTimezone"])
@ has_permissions(manage_messages=True)
async def _removeTimezone(ctx, timezone):
    timeZones = settings["guilds"][getGuildIndex(ctx.guild)]["timeZones"]
    if timezone not in timeZones:
        return
    timeZones.remove(timezone)
    writeJsonDoc()


@ bot.command(name="currentTimezones", aliases=["ct", "CT", "cT", "CURRENTTIMEZONES", "currenttimezones", "CurrentTimezones"])
@ has_permissions(manage_messages=True)
async def _currentTimezones(ctx):
    timeZones = settings["guilds"][getGuildIndex(ctx.guild)]["timeZones"]
    for timezone in timeZones:
        print(timezone)

bot.run(tokens.test)
