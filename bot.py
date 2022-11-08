from time import sleep
from config import token, prefix, api_key, role_id
from datetime import datetime
import discord
import requests
from discord.ext import commands

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")
used = []

try:
    with open('used.txt', 'r') as f:
        used = f.read().splitlines()
except:
    pass

@client.event
async def on_ready():
    print('[-] Bot Started')
    print(f'[-] Logged in as {client.user}')
    await client.change_presence(activity=discord.Game(f'{prefix}help for info'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        e = discord.Embed(title="Missing Arguments", description=f"Please run the command again with all the required arguments\nType`{prefix}help` to know more", color=0xff001e, timestamp=datetime.utcnow())
        e.set_footer(text=ctx.author.name ,icon_url=ctx.author.avatar.url)
        await ctx.send(embed=e)
    else:
        raise error


@client.command()
async def help(ctx):
    e = discord.Embed(title="Commands", description="", color=0xCC9EFF, timestamp=datetime.utcnow())
    e.add_field(name=f"{prefix}claim <order_id>", value="`Claim the client role`", inline=False)
    e.set_footer(text=ctx.author.name ,icon_url=ctx.author.avatar.url)
    await ctx.send(embed=e)


@client.command()
async def claim(ctx, order_id):
    order_id = order_id.strip()
    if order_id in used:
        e = discord.Embed(title="Invalid Order ID", description=f"This order ID has already been used", color=0xff001e, timestamp=datetime.utcnow())
        e.set_footer(text=ctx.author.name ,icon_url=ctx.author.avatar.url)
        await ctx.send(embed=e)
        return
        
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    while True:
        try:
            response = requests.get(f"https://sell.app/api/v1/invoices/{order_id}", headers=headers)
            break
        except:
            sleep(1)
            error += 1
            if error >= 5:
                e = discord.Embed(title="Role not given", description=f"Something went wrong while trying to give you the **Client** role.\nPlease try again after some time.", color=0xff001e, timestamp=datetime.utcnow())
                e.set_footer(text=ctx.author.name ,icon_url=ctx.author.avatar.url)
                await ctx.send(embed=e)
                return
            
    if response.status_code == 200:
        try:
            client_role = ctx.guild.get_role(role_id)
            await ctx.author.add_roles(client_role)
            used.append(order_id)
            e = discord.Embed(title="Role Given", description=f"Successfully Claimed **Client** Role", color=0xCC9EFF, timestamp=datetime.utcnow())
            with open('used.txt', 'a') as f:
                f.write(order_id + '\n')
        except:
            e = discord.Embed(title="Role not given", description=f"Something went wrong while trying to give you the **Client** role.\nPlease try again after some time.", color=0xff001e, timestamp=datetime.utcnow())
    else:
        e = discord.Embed(title="Invalid Order ID", description=f"You have entered an Invalid order ID", color=0xff001e, timestamp=datetime.utcnow())

    e.set_footer(text=ctx.author.name ,icon_url=ctx.author.avatar.url)
    await ctx.send(embed=e)


client.run(token)