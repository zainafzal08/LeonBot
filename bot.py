import discord
import asyncio
import re
import random
from Db import Db
import os

# Globals
db = Db()
client = discord.Client()

# Helper
def hide(t):
    return "A"*len(t)

def extractQuestion(t):
    m = t.lower()
    m = re.sub(r'\s+',' ',m)
    m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
    m = m.strip()
    return m

def getAllItems():
    result = db.allItems()
    return result

def registerPlayer(name):
    db.newPlayer(name)

def postItem():
    allItems = getAllItems()
    i = random.randint(0,len(allItems)-1)
    item = allItems[i]
    db.removeItem(item[0])
    name = item[0]
    description = item[1]
    items = []
    items.append("```")
    items.append(">> "+name)
    items.append("="*(5+len(name)))
    items.append("\n")
    items.append(description)
    items.append("```")
    return "\n".join(items)

def subtractToken(name):
    db.editTokens(name, -1)

def tokenSummary():
    players = db.allPlayers()
    response = []
    response.append("```")
    for player in players:
        if player  == "":
            continue
        response.append("%-15s | %s"%(player[0],player[1]))
    response.append("```")
    if len(response) < 3:
        response = []
        response.append("I don't know any players! say `leon bot say hello to <player>` to introduce me")
    return "\n".join(response)

# Trigger Functions

async def newPlayer(message, trigger):
    name = re.search(r'say hello to (\w+)',trigger).group(1)
    res = registerPlayer(name)
    if res == -1:
        await client.send_message(message.channel, "I already know a "+name+"!")
    else:
        await client.send_message(message.channel, "Hello "+name+"!")

async def takeTokens(message, trigger):
    name = re.search(r'give (\w+) an item',trigger).group(1)
    tokens = db.playerTokens(name)
    if tokens > 0:
        subtractToken(name)
        await client.send_message(message.channel, postItem())
    elif tokens == 0:
        await client.send_message(message.channel, "That person doesn't have any tokens!")
    elif tokens == -1:
        await client.send_message(message.channel, "I don't know who that is")

async def giveTokens(message, trigger):
    players = db.allPlayers()
    for player in players:
        db.editTokens(player[0],1)
    await client.send_message(message.channel, "Done!")

async def showTokens(message, trigger):
    s = tokenSummary()
    await client.send_message(message.channel, s)


# triggers
triggers = [
    ("leon bot tokens for all", giveTokens),
    ("leonbot tokens for all", giveTokens),
    ("leon-bot tokens for all", giveTokens),
    ("leon bot give \w+ an item", takeTokens),
    ("leonbot give \w+ an item", takeTokens),
    ("leon-bot give \w+ an item", takeTokens),
    ("leon bot say hello to \w+", newPlayer),
    ("leonbot say hello to \w+", newPlayer),
    ("leon-bot say hello to \w+", newPlayer),
    ("leon bot how many tokens does everyone have", showTokens),
    ("leonbot how many tokens does everyone have", showTokens),
    ("leon-bot how many tokens does everyone have", showTokens)
]

# Discord event handllers
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client)

@client.event
async def on_message(message):
    # ignore bots
    if (message.author.bot):
        return
    m = extractQuestion(message.content)
    for trigger in triggers:
        if re.search(trigger[0], m) and re.search(trigger[0], m).group(0):
            await trigger[1](message,m)

client.run(os.environ.get('BOT_TOKEN'))
client.close()
