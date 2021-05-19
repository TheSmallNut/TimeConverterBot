import discord
import json
import tokens
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


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
    return settings["guilds"][getGuildIndex]


bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix)


@ bot.event
async def on_guild_join(guild):
    settings["guilds"].append({})
    location = settings["guilds"][-1]
    location["id"] = guild.id
    location["name"] = guild.name
    location["prefix"] = "$"
    location["region"] = guild.region
    location["timeZones"] = []
