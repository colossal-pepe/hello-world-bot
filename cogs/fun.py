import discord
import praw
import time
import os
from urllib.request import urlopen as uReq
import urllib.request
from bs4 import BeautifulSoup as soup
from discord.ext import commands

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", None)
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", None)

r = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent='Fetch Dank Memes Bot')

class Reddit:

    def __init__(self):
        pass

    def getDankMeme():
        slink = 'Could not find meme. Try again.'
        sr = r.subreddit('dankmemes').random()
        if not sr.is_self:
            slink = sr.url
        return slink

    def getMeme():
        slink = 'Could not find meme. Try again.'
        sr = r.subreddit('memes').random()
        if not sr.is_self:
            slink = sr.url
        return slink


class Misc:

    def __init__(self):
        pass

    def getJoke():
        uClient = uReq("http://www.allthejokes.com/")
        page_html = uClient.read()
        uClient.close()
        page = soup(page_html, "html.parser")
        joke_div = page.find("div", {"class": "joke"})
        return joke_div.find("p").getText()

    def inspirobot():
        opener = AppURLopener()
        uClient = opener.open("https://inspirobot.me/api?generate=true")
        page_bytes = uClient.read()
        uClient.close()
        return page_bytes.decode("utf-8")


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["dankmemes"], brief="Get some dank memes")
    async def dankmeme(self, ctx):
        await ctx.trigger_typing()
        post_url = Reddit.getDankMeme()
        await ctx.send(post_url)

    @commands.command(aliases=["memes"], brief="Get some memes")
    async def meme(self, ctx):
        await ctx.trigger_typing()
        post_url = Reddit.getMeme()
        await ctx.send(post_url)

    @commands.command(brief="Laugh")
    async def joke(self, ctx):
        await ctx.trigger_typing()
        joke = Misc.getJoke()
        await ctx.send(joke)

    @commands.command(brief="Get inspired")
    async def inspireme(self, ctx):
        await ctx.trigger_typing()
        quote = Misc.inspirobot()
        await ctx.send(quote)


def setup(client):
    client.add_cog(Fun(client))
