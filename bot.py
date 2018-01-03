import discord
import asyncio


# Globals
client = discord.Client()

# Discord event handlers
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client)

@client.event
async def on_message(message):
    await client.send_message(message.channel, "HELLO")

client.run(<APP TOKEN HERE>)
client.close()
