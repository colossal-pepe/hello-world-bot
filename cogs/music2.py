import discord
import json
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", None)

guild2members = {}

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))

def fetchConnections():
    global guild2members
    with open("spotifyconnections.json", "r") as sc:
        guild2members = json.load(sc)

def dumpConnections():
    global guild2members
    with open("spotifyconnections.json", "w") as sc:
        json.dump(guild2members, sc)

def update(gid, members):
    for man in members:
        if man.display_name not in guild2members[gid]:
            guild2members[gid][man.display_name] = "NULL"

def getPlaylistEmbedOfMember(name, pld):
    plinfo = []
    for item in pld['items']:
        plinfo.append([item['name'], item['external_urls']['spotify']])
    return IndividualEmbed(f"{name}'s playlists", "None", plinfo)

def parseUrl(s):
    index = 30
    for c in s[30:]:
        if c == '?':
            break
        index += 1
    return s[30:index]

class IndividualEmbed:

    def __init__(self, title, desc, fields):
        self.title = title
        self.desc = desc
        self.fields = fields
    
    def makeEmbed(self):
        embed = discord.Embed(title=self.title)
        for field in self.fields:
            embed.add_field(name=field[0], value=field[1], inline=False)
        return embed

class Music2(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Share your spotify profile")
    async def shareprofile(self, ctx, *, url):
        guildid = str(ctx.guild.id)
        author = ctx.message.author.nick
        if str(guildid) not in guild2members:
            guild2members[str(guildid)] = {}
        if sorted(guild2members[str(guildid)].keys()) != sorted([man.display_name for man in ctx.guild.members]):
            update(str(guildid), ctx.guild.members)
        parsedUrl = parseUrl(url)
        try:
            spotify.user(parsedUrl)
        except spotipy.exceptions.SpotifyException as err:
            await ctx.send("No such user.")
            return
        guild2members[str(guildid)][ctx.message.author.nick] = parsedUrl
        await ctx.send(f"Fetched profile of {parsedUrl}.")
        dumpConnections()
    
    @commands.command(brief="Get playlists of tagged person")
    async def getplaylistsfor(self, ctx, *, member: discord.Member):
        if str(ctx.guild.id) not in guild2members:
            await ctx.send("No members have yet shared their profile on this server.")
            return
        if guild2members[str(ctx.guild.id)][member.display_name] == "NULL":
            await ctx.send("Their profile is not shared in this server.")
            return
        playlistDict = spotify.user_playlists(guild2members[str(ctx.guild.id)][member.display_name])
        embedObj = getPlaylistEmbedOfMember(member.display_name, playlistDict)
        await ctx.send(embed=embedObj.makeEmbed())
    
    @commands.command(brief="Get all playlists")
    async def getallplaylists(self, ctx):
        if str(ctx.guild.id) not in guild2members:
            await ctx.send("No members have yet shared their profile on this server")
            return
        for key in guild2members[str(ctx.guild.id)]:
            if guild2members[str(ctx.guild.id)][key] == "NULL":
                continue
            playlistsDict = spotify.user_playlists(guild2members[str(ctx.guild.id)][key])
            embedObj = getPlaylistEmbedOfMember(key, playlistsDict)
            await ctx.send(embed=embedObj.makeEmbed())
    
    @commands.command(brief="Help for commands in this module")
    async def helpmusic(self, ctx):
        embedObj = discord.Embed(title="Helper Man", description="Note: do no share your profile if you suspect that you might make any of your already shared playlists secret because the link will be perpetually saved in chat and it won't be that secret. Thank you for understanding this bot's bad engineering.")
        embedObj.add_field(name="?shareprofile", value="?shareprofile [ur spotify share link]", inline=False)
        embedObj.add_field(name="?getplaylistsfor", value="?getplaylistsfor [@the person whose playlist u wanna get]", inline=False)
        await ctx.send(embed=embedObj)
    

def setup(client):
    client.add_cog(Music2(client))
    fetchConnections()
