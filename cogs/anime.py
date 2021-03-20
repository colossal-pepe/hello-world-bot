import discord
import time
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from discord.ext import tasks, commands

anime2info = {}

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def getEpisodeTally(url):
    try:
        opener = AppURLopener()
        page = opener.open(url)
        page_html = soup(page, "html.parser")
        return int(page_html.find("div", {"id": "epslistplace"}).decode()[35:37])
    except Exception:
        return -1

def fetchAnimeTrackingInfo():
    global anime2info
    with open("animetrackinginfo.json", "r") as ati:
        anime2info = json.load(ati)

def dumpAnimeTrackingInfo():
    global anime2info
    with open("animetrackinginfo.json", "w") as ati:
        json.dump(anime2info, ati)

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.animeupdates.start()
    
    @commands.command(brief="Track anime given animixplay link and name")
    async def trackanime(self, ctx, url, *, name):
        await ctx.trigger_typing()
        if url in anime2info and str(ctx.guild.id) in anime2info[url]["guilds"]:
            await ctx.send("Anime already being tracked for this server.")
            return
        if url not in anime2info:
            epnum = getEpisodeTally(url)
            if epnum == -1:
                await ctx.send("Invalid url.")
                return
            anime2info[url] = {"eps": getEpisodeTally(url), "guilds": {}}
        anime2info[url]["guilds"][str(ctx.guild.id)] = {"name": name, "channel": ctx.channel.id}
        dumpAnimeTrackingInfo()
        await ctx.send(f"Started tracking {name} at {url}.")
    
    @commands.command(brief="Stop tracking anime")
    async def forgetanime(self, ctx, url):
        await ctx.trigger_typing()
        if url not in anime2info or str(ctx.guild.id) not in anime2info[url]["guilds"]:
            await ctx.send("It wasn't being tracked in the first place stop bothering me.")
            return
        del anime2info[url]["guilds"][str(ctx.guild.id)]
        if not anime2info[url]["guilds"]:
            del anime2info[url]
        dumpAnimeTrackingInfo()
        await ctx.send("Forgetting complete.")
    
    @tasks.loop(minutes=15.0)
    async def animeupdates(self):
        print("came here")
        for url in anime2info:
            prevEp = anime2info[url]["eps"]
            currentEp = getEpisodeTally(url)
            if currentEp == prevEp or currentEp == -1:
                continue
            for guild in anime2info[url]["guilds"]:
                channel = self.client.get_channel(anime2info[url]["guilds"][guild]["channel"])
                await channel.send(f"@everyone A new episode of {anime2info[url]['guilds'][guild]['name']} has been released!")
            anime2info[url]["eps"] = currentEp
        dumpAnimeTrackingInfo()

    @animeupdates.before_loop
    async def beforeAnimeupdates(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Anime(client))
    fetchAnimeTrackingInfo()
