import discord
import time
import wolframalpha
import os
from discord.ext import commands

qA = []

question = ""

aInfo = []

clientToken = os.environ.get("WOLFRAM_ALPHA_CLIENT", None)

cl = wolframalpha.Client(clientToken)


class Intelligence(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Ask Intelligence")
    async def ask(self, ctx, *, qs: str):
        await ctx.trigger_typing()
        msg = inquire(qs)
        await ctx.send(msg)

    @commands.command(brief="Get answers for query")
    async def ans(self, ctx, *, i: str):
        nok = False
        try:
            int(i)
            qA[0]
        except:
            nok = True
        if (nok):
            ctx.send("No")
            return
        await ctx.trigger_typing()
        await ctx.send(f"Results for {aInfo[int(i)-1]}:")
        for url in qA[int(i)-1]:
            await ctx.send(url)


def parseInfo(ai, query):
    msg = f"The following information is available about the query '{query}':"
    size = len(ai)
    for i in range(size):
        aInfo.append(ai[i])
        msg += f"\n{i+1}. {ai[i]}"
    msg += f"\nUse '?ans (number)' to get the results for that part."
    return msg


def inquire(q):
    qA.clear()
    aInfo.clear()
    question = q
    res = cl.query(q)
    availableInfo = []
    if not 'pod' in res:
        return "No"
    for pod in res['pod']:
        availableInfo.append(pod['@title'])
        if (int(pod['@numsubpods']) > 1):
            info = [sub['img']['@src'] for sub in pod['subpod']]
        else:
            info = [pod['subpod']['img']['@src']]
        qA.append(info)
    msg = parseInfo(availableInfo, q)
    return msg


def setup(client):
    client.add_cog(Intelligence(client))
