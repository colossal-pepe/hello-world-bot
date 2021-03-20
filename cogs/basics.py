import discord
import random
from discord.ext import commands

class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="See latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["8ball"], brief="Get your opinions from a non-living thing")
    async def eightball(self, ctx):
        eightBallResponses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."]
        await ctx.send(f"{random.choice(eightBallResponses)}")

    @commands.command()
    async def detect(self, ctx):
        responses = ["That's a lie", "That's true"]
        await ctx.send(f'{random.choice(responses)}')
    
    @commands.command()
    async def clear(self, ctx, amount = 5):
        await ctx.channel.purge(limit = amount+1)

def setup(client):
    client.add_cog(Basics(client))