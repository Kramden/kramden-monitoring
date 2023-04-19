import os
import discord
from lars import apache

basedir="/var/www/html/ubuntu-autoinstall-ipxe"
lunarpath=os.path.join(basedir, "ubuntu/23.04")
jammypath=os.path.join(basedir, "ubuntu/22.04")

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
    if message.content.startswith('-isocheck'):
        await message.channel.send(mount_status())

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

def check_mount(dir_path):
    return os.path.ismount(dir_path)

def mount_status():
    output = "```\n"
    lunar_mounted = check_mount(os.path.join(lunarpath, "iso"))
    if not lunar_mounted:
        output += "Ubuntu 23.04 iso is not mounted, to fix:\n\n"
        output += "sudo mount -o loop %s/lunar-desktop-amd64.iso %s/iso\n\n" %(lunarpath, lunarpath)
    else:
        output += "Ubuntu 23.04 iso is mounted\n\n"
    
    jammy_mounted = check_mount(os.path.join(jammypath, "iso"))
    if not jammy_mounted:
        output += "Ubuntu 22.04 iso is not mounted, to fix:\n\n"
        output += "sudo mount -o loop %s/lunar-desktop-amd64.iso %s/iso\n\n" %(jammypath, jammypath)
    else:
        output += "Ubuntu 22.04 iso is mounted\n\n"
    output += "\n```"
    return output

token = os.getenv('KRAMDEN_DISCORD_TOKEN')
if token:
  client.run(token)
else:
  print("KRAMDEN_DISCORD_TOKEN environment variable required")

