import os
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

usage = '''\
Welcome to the Kramden bot!

Available commands:
    -stats 
    -up
'''.format(length='multi-line', ordinal='second')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-stats'):
        await message.channel.send('FIXME')

    if message.content.startswith('-up'):
        await message.channel.send('FIXME')
    if message.content.startswith('-help'):
        await message.channel.send(usage)

token = os.getenv('KRAMDEN_DISCORD_TOKEN')
if token:
  client.run(token)
else:
  print("KRAMDEN_DISCORD_TOKEN environment variable required")
