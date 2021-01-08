# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
from bs4 import BeautifulSoup
import requests
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

url = "https://www.newegg.com/p/pl?d=3080&N=100007709%204841&isdeptsrh=1&PageSize=96"


@tasks.loop(minutes=1)
async def check_stock():
    channel = bot.get_channel(INSERT CHANNEL ID)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    role = discord.utils.get(guild.roles, name='Notify')
    notify = False
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.findAll('div',id = True, attrs = {'class': 'item-cell'})
    n = len(items)-1
 
    #await channel.send("Checking at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("Checking at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
          
    for item in items:
        # item_name = str(item.findAll('a',attrs = {'class': 'item-title'})[0].text)
        if 'OUT OF STOCK' in str(item): 
            continue
        else: 
            notify = True
            item_link = str(item.findAll('a', href=True)[0]['href'])
            item_price = str(item.findAll('li',attrs = {'class': 'price-current'})[0].findAll('strong')[0])[8:-9]
            await channel.send('$'+item_price)
            await channel.send(item_link)
    if notify:
        await channel.send('Stock Found {}'.format(role.mention))

@bot.event
async def on_raw_reaction_add(payload):
    EMOJI = '✅'
    if payload.emoji.name == EMOJI:
        member = payload.member
        guild = discord.utils.get(bot.guilds, name=GUILD)
        channel = bot.get_channel(INSERT CHANNEL ID)
        role = discord.utils.get(guild.roles, name='Notify')

        await member.add_roles(role)
        await channel.send('{} added to {} role'.format(member, role))
            
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    channel = bot.get_channel(INSERT CHANNEL ID)
    print(f'{bot.user} has connected to {guild.name}')
#     await channel.send('✅ this message to be added to alert list')
#     await channel.send('If you mute this channel and have the notify role then you will still see the red notification box next to the channel without the noise')
    check_stock.start()
    
bot.run(TOKEN)
