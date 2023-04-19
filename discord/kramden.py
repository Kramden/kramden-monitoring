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
        await message.channel.send(get_stats())

    if message.content.startswith('-up'):
        await message.channel.send('FIXME')
    if message.content.startswith('-help'):
        await message.channel.send(usage)

def get_stats():
    jammy = 0
    lunar = 0
    windows = 0
    pmagic = 0
    memtest = 0

    with open('/var/log/apache2/access.log') as f:
        with apache.ApacheSource(f) as source:
            for row in source:
                #print(row[4])
                if '/ubuntu/22.04/iso/casper/vmlinuz' in str(row[4]):
                    jammy = jammy + 1
                if '/ubuntu/23.04/iso/casper/vmlinuz' in str(row[4]):
                    lunar = lunar + 1
                if 'windows' in str(row[4]):
                    windows = windows + 1
                if 'pmagic' in str(row[4]):
                    pmagic = pmagic + 1
                if 'memtest' in str(row[4]):
                    memtest = memtest + 1

    output = '''\
Total stats for today:
Ubuntu 22.04: {jammy}
Ubuntu 23.04: {lunar}
Windows: {windows}
Parted Magic: {pmagic}
memtest: {memtest}
'''.format(length='multi-line', ordinal='second', jammy=jammy, lunar=lunar, windows=windows, pmagic=pmagic, memtest=memtest)
    print(output)
    return output

token = os.getenv('KRAMDEN_DISCORD_TOKEN')
if token:
    client.run(token)
else:
    print("KRAMDEN_DISCORD_TOKEN environment variable required")
