import discord
import random
import os
from discord.ext import commands

intents = discord.Intents().all()

client = commands.Bot(command_prefix='?', intents=intents)

TOKEN = os.environ.get("DISCORD_BOT_TOKEN", None)

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def restart(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
