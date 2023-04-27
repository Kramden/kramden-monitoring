import os
import discord
from discord.ext import tasks, commands
from lars import apache
import requests

basedir="/var/www/html/ubuntu-autoinstall-ipxe"
lunarpath=os.path.join(basedir, "ubuntu/23.04")
jammypath=os.path.join(basedir, "ubuntu/22.04")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

usage = '''\
Welcome to the Kramden bot!

Available commands:
    $stats
    $isocheck
'''.format(length='multi-line', ordinal='second')

@client.event
async def on_ready():
    task_loop.start()
    print('We have logged in as {0.user}'.format(client))

@tasks.loop(seconds=30) # '30' is the time interval in seconds.
async def task_loop():
    channel = client.get_channel(1098262455857205360)

    if check_mounts():
        embed = discord.Embed(title = "ISO Status: ", description = mount_status(), color = 0xFF5733)
        await channel.send(embed = embed)

    if not check_apache():
        embed = discord.Embed(title = "Apache is down: ", description = "Web service is offline", color = 0xFF5733)
        await channel.send(embed = embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.channel.id)
    print(message.content)

    if message.content.startswith('$stats'):
        embed = discord.Embed(title = "Total Stats for Today:", description = get_stats(), color = 0xFF5733)
        await message.channel.send(embed = embed)
    if message.content.startswith('$help'):
        await message.channel.send(usage)
    if message.content.startswith('$isocheck'):
        embed = discord.Embed(title = "ISO Status: ", description = mount_status(), color = 0xFF5733)
        await message.channel.send(embed = embed)

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
Ubuntu 22.04: {jammy}
Ubuntu 23.04: {lunar}
Windows: {windows}
Parted Magic: {pmagic}
memtest: {memtest}
'''.format(length='multi-line', ordinal='second', jammy=jammy, lunar=lunar, windows=windows, pmagic=pmagic, memtest=memtest)
    print(output)
    return output

def check_apache():
  try:
    response = requests.get("http://192.168.1.254")
    return response.status_code == 200
  except:
      return False
  return True

def check_mounts():
    if not check_mount(os.path.join(lunarpath, "iso")) or not check_mount(os.path.join(jammypath, "iso")):
        return True

def check_mount(dir_path):
    return os.path.ismount(dir_path)

def mount_status():
    output = ""
    lunar_mounted = check_mount(os.path.join(lunarpath, "iso"))
    if not lunar_mounted:
        output += "Ubuntu 23.04 iso is not mounted, to fix:\n\n"
        output += "```fix\nsudo mount -o loop %s/lunar-desktop-amd64.iso %s/iso\n```\n\n" %(lunarpath, lunarpath)
    else:
        output += "Ubuntu 23.04 iso is mounted\n\n"
    
    jammy_mounted = check_mount(os.path.join(jammypath, "iso"))
    if not jammy_mounted:
        output += "Ubuntu 22.04 iso is not mounted, to fix:\n\n"
        output += "```fix\nsudo mount -o loop %s/lunar-desktop-amd64.iso %s/iso\n```\n\n" %(jammypath, jammypath)
    else:
        output += "Ubuntu 22.04 iso is mounted\n\n"
    return output

token = os.getenv('KRAMDEN_DISCORD_TOKEN')
if token:
    client.run(token)
else:
    print("KRAMDEN_DISCORD_TOKEN environment variable required")
