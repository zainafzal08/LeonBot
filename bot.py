import discord
import asyncio
import re
import random

# Helper
def extractQuestion(t):
    m = t.lower()
    m = re.sub(r'\s+',' ',m)
    m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
    m = m.strip()
    return m

def getAllItems():
    f = open("data.txt","r")
    text = f.read().strip()
    f.close()
    rawItems = text.split("\n\n")
    result = []
    for item in rawItems:
        result.append((item.split("\n")[0],"\n".join(item.split("\n")[1:])))
    return result

def registerPlayer(name):
    f = open("players.txt","a")
    f.write(name+",0\n")
    f.close()

def postItem():
    allItems = getAllItems()
    i = random.randint(0,len(allItems)-1)
    item = allItems[i]
    del allItems[i]
    writeAllItems(allItems)
    writeDoneItem(item)
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

def playerTokens(name):
    f = open("players.txt","r")
    raw = f.read().strip()
    f.close()
    players = raw.split("\n")
    for player in players:
        if player.split(",")[0] == name:
            return int(player.split(",")[1])
    return -1

def subtractToken(name):
    f = open("players.txt","r")
    raw = f.read().strip()
    f.close()
    players = raw.split("\n")
    new = []
    for player in players:
        if player.split(",")[0] == name:
            new.append((player.split(",")[0],str(int(player.split(",")[1])-1)))
        else:
            new.append((player.split(",")[0],str(int(player.split(",")[1]))))

    f = open("players.txt","w")
    for player in new:
        f.write(player[0]+","+player[1]+"\n")
    f.close()

def tokenSummary():
    f = open("players.txt","r")
    raw = f.read().strip()
    f.close()
    players = raw.split("\n")
    response = []
    response.append("```")
    for player in players:
        response.append("%-15s | %s"%(player.split(",")[0],player.split(",")[1]))
    response.append("```")

    return "\n".join(response)

def writeAllItems(allItems):
    f = open("data.txt","w")
    for item in allItems:
        f.write(item[0]+"\n")
        f.write(item[1]+"\n\n")
    f.close()


def writeDoneItem(item):
    f = open("done.txt","a")
    f.write(item[0]+"\n")
    f.write(item[1]+"\n\n")
    f.close()

# Trigger Functions

async def newPlayer(message, trigger):
    name = re.search(r'say hello to (\w+)',trigger).group(1)
    registerPlayer(name)
    await client.send_message(message.channel, "Hello "+name+"!")

async def takeTokens(message, trigger):
    name = re.search(r'give (\w+) an item',trigger).group(1)
    tokens = playerTokens(name)
    if tokens > 0:
        subtractToken(name)
        await client.send_message(message.channel, postItem())
    elif tokens == 0:
        await client.send_message(message.channel, "That person doesn't have any tokens!")
    elif tokens == -1:
        await client.send_message(message.channel, "I don't know who that is")

async def giveTokens(message, trigger):
    f = open("players.txt","r")
    raw = f.read().strip()
    f.close()
    players = raw.split("\n")
    new = []
    for player in players:
        new.append((player.split(",")[0],str(int(player.split(",")[1])+1)))

    f = open("players.txt","w")
    for player in new:
        f.write(player[0]+","+player[1]+"\n")
    f.close()
    await client.send_message(message.channel, "Done!")

async def giveTokens(message, trigger):
    f = open("players.txt","r")
    raw = f.read().strip()
    f.close()
    players = raw.split("\n")
    new = []
    for player in players:
        new.append((player.split(",")[0],str(int(player.split(",")[1])+1)))

    f = open("players.txt","w")
    for player in new:
        f.write(player[0]+","+player[1]+"\n")
    f.close()
    await client.send_message(message.channel, "Done!")

async def showTokens(message, trigger):
    s = tokenSummary()
    await client.send_message(message.channel, s)

# Globals
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
client = discord.Client()

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

client.run("Mzk4MDQwMzg3NTc2Mzk3ODQ1.DS4vkg.7ul--xPSOiEiFXFcAXHsNyOlxe8")
client.close()
