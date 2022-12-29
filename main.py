import discord
from replit import db
from discord.ext import commands
import keepalive
import os, requests, random, time
import traceback
keepalive.keep_alive()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='+', intents=intents)
pendingrequests = {}
cpn = None
gcpn = None
gpendingrequests = {}


class Devs(discord.ui.View):
    @discord.ui.select(
        placeholder = "Select Developer Type",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Scripter",
                description="Writes scripts in roblox!"
            ),
            discord.SelectOption(
                label="Builder",
                description="Puts together parts in roblox"
            ),
            discord.SelectOption(
                label="Modeler",
                description="Makes models in external software and imports them to roblox"
            ),
            discord.SelectOption(
                label="UI Designer",
                description="Makes neat 2d designs in roblox"
            ),
            discord.SelectOption(
                label="Animator",
                description="Animates your models in roblox"
            ),
            discord.SelectOption(
                label="GFX Designer",
                description="Makes a good job of particles in roblox"
            ),
            discord.SelectOption(
                label="SFX Designer",
                description="Designs sound ambients and effects in roblox"
            ),
            discord.SelectOption(
                label="Programmer",
                description="Creates programs outside of roblox"
            ),
            discord.SelectOption(
                label="Other",
                description="More than 1 type of dev, or role is not on list"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        global cpn, pendingrequests
        pendingrequests[cpn]['point'] = 2
        pendingrequests[cpn]['dev'] = select.values[0]
        cpn = None
        embed = discord.Embed(title="Describe request", description="Describe it as fully as possible. respond with 'cancel' to cancel")
        await interaction.response.send_message(embed=embed)


class GDevs(discord.ui.View):
    @discord.ui.select(
        placeholder = "Select Developer Type That Best Fits You",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Scripter",
                description="Writes scripts in roblox!"
            ),
            discord.SelectOption(
                label="Builder",
                description="Puts together parts in roblox"
            ),
            discord.SelectOption(
                label="Modeler",
                description="Makes models in external software and imports them to roblox"
            ),
            discord.SelectOption(
                label="UI Designer",
                description="Makes neat 2d designs in roblox"
            ),
            discord.SelectOption(
                label="Animator",
                description="Animates your models in roblox"
            ),
            discord.SelectOption(
                label="GFX Designer",
                description="Makes a good job of particles in roblox"
            ),
            discord.SelectOption(
                label="SFX Designer",
                description="Designs sound ambients and effects in roblox"
            ),
            discord.SelectOption(
                label="Programmer",
                description="Creates programs outside of roblox"
            ),
            discord.SelectOption(
                label="Other",
                description="More than 1 type of dev, or role is not on list"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        global gcpn, gpendingrequests
        gpendingrequests[gcpn]['point'] = 2
        gpendingrequests[gcpn]['dev'] = select.values[0]
        gcpn = None
        embed = discord.Embed(title="Give Info about yourself", description="Describe yourself as fully as possible. respond with 'cancel' to cancel")
        await interaction.response.send_message(embed=embed)

@bot.command()
async def verify(ctx, arg):
    try:
        key = arg + '+temp'
        rname = db[key]
        dname = ctx.author
        db[rname] = str(dname)
        key2 = str(dname) + '+rbx'
        db[key2] = rname
        del db[key]
        await ctx.send("Successfully Connected to " + rname)
    except Exception as e:
        await ctx.send(e.message + ' ' + e.args)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(939754863301124128)
    embed = discord.Embed(description=f"**{member.mention} joined the server\n\nAccount creation:**\n\n{member.created_at}\nUser Id: {member.id}", color=0x2ecc71)
    try:
      embed.set_author(name=member, icon_url=member.avatar.url)
    except:
      embed.set_author(name=member)
    await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def test(ctx):
    member = ctx.author
    channel = bot.get_channel(939754863301124128)
    embed = discord.Embed(description=f"**{member.mention} joined the server\n\nAccount creation:**\n\n{member.created_at}\nUser Id: {member.id}", color=0x2ecc71)
    try:
      embed.set_author(name=member, icon_url=member.avatar.url)
    except:
      embed.set_author(name=member)
    await channel.send(embed=embed)

@bot.command()
async def getroblox(ctx, member: discord.Member):
      key2 = str(member) + '+rbx'
      try:
        await ctx.send('roblox username = ' + db[key2])
      except:
        await ctx.send('Failed To Fetch Username')

@bot.command()
async def getdiscord(ctx, arg):
      try:
        await ctx.send('discord username = ' + db[arg])
      except:
        await ctx.send('Failed To Fetch Username')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} has been banned for {reason}')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="roblox events"))

@bot.command()
async def site(ctx):
      await ctx.send('Check out the website now! >>> https://sites.google.com/view/thedeveloperproject/Home?authuser=0')

@bot.command()
async def tiktok(ctx):
      await ctx.send('Check out the tiktok now! >>> https://tiktok.com/@cjcreatess')

@bot.command()
async def formating(ctx):
      embed=discord.Embed(title="How to format code on discord",description="1. Make sure to use the <#1044083721428537444> channel unless it is related to something on another channel.\n\n2. Please format your code like this: \```lua print('hello world!') \```\n\n3. Make sure to fully explain your code\n\n4. If you are helping someone, try not to complete the whole thing for them, they won't learn like this")
      await ctx.send(embed=embed)


@bot.command()
async def verifylink(ctx):
      await ctx.send('Please link your roblox account >>> https://www.roblox.com/games/11713687819/TDP-Verify')

@bot.command()
async def ping(ctx):
      await ctx.send(f"Pong! Latency is {bot.latency}")

@bot.command()
async def compile(ctx, *, arg):
      arg2 = arg.split('\n')[1:]
      arg2.pop()
      code = ''
      for x in arg2:
        code += x + '\n'
      try:
        key = str(random.randint(10000, 99999999))
        temp = 'temp{}.lua'.format(key)
        f = open(temp, 'w')
        f.write(code)
        f.close()
        files = {'file': open(temp, 'rb')}
        r = requests.post(f'https://CompilerBot.galacticapricot.repl.co/clua', files=files)
        os.remove(temp)
        await ctx.send(f"Compiled! Output: ```lua\n{r.text}```")
      except Exception as e:
        print(e)
        await ctx.send("Failed To Compile.")

@bot.command()
async def compilepy(ctx, *, arg):
      arg2 = arg.split('\n')[1:]
      arg2.pop()
      code = ''
      for x in arg2:
        code += x + '\n'
      try:
        key = str(random.randint(10000, 99999999))
        temp = 'temp{}.py'.format(key)
        f = open(temp, 'w')
        f.write(code)
        f.close()
        files = {'file': open(temp, 'rb')}
        r = requests.post(f'https://CompilerBot.galacticapricot.repl.co/cpy', files=files)
        os.remove(temp)
        await ctx.send(f"Compiled! Output: ```py\n{r.text}```")
      except Exception as e:
        print(e)
        await ctx.send("Failed To Compile.")

@bot.command()
async def bubblepopping(ctx):
    embed=discord.Embed(title="bubble popping",description="||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||")
    await ctx.send(embed=embed)

@bot.command()
async def request(ctx, rbx, *, info):
      if ctx.channel.id != 1046117793784938546:
        await ctx.send('Please only use the request channel to send requests.')
        return
      try:
        int(rbx)
        info2 = info
        info += f'\n\n\n**Payment:** {rbx}\n\n**Contact:** {ctx.author.mention}'
        try:
          key = ctx.author.name + '+rbx'
          roblox = db[key]
          info += f'\n\n**Roblox:** {roblox}'
        except:
          pass
        embed=discord.Embed(title=f"{ctx.author.name}'s ticket",description=info)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        channel = bot.get_channel(1046118645081849906)
        await channel.send(embed=embed)
        await ctx.send(f'Sent request for {rbx} robux to create {info2}')
      except:
        await ctx.send('Failed to send. Usage: +request robux info')


@bot.slash_command(name='guildid')
@commands.has_permissions(kick_members=True)
async def guildid(ctx):
    await ctx.respond(ctx.guild.id)


@bot.slash_command(name='hire')
async def hire(ctx):
    global pendingrequests, cpn
    embed=discord.Embed(title="Continue in dm's")
    pendingrequests[ctx.author.id] = {'point': 1}
    await ctx.respond(embed=embed)
    cpn = ctx.author.id
    await ctx.author.send("Select developer type", view=Devs())

@bot.slash_command(name='gethired')
async def gethired(ctx):
    global gpendingrequests, gcpn
    embed=discord.Embed(title="Continue in dm's")
    gpendingrequests[ctx.author.id] = {'point': 1}
    await ctx.respond(embed=embed)
    gcpn = ctx.author.id
    await ctx.author.send("Select developer type", view=GDevs())

@bot.slash_command(name='formating')
async def formating2(ctx):
      embed=discord.Embed(title="How to format code on discord",description="1. Make sure to use the <#1044083721428537444> channel unless it is related to something on another channel.\n\n2. Please format your code like this: \```lua print('hello world!') \```\n\n3. Make sure to fully explain your code\n\n4. If you are helping someone, try not to complete the whole thing for them, they won't learn like this")
      await ctx.respond(embed=embed)

@bot.slash_command(name="tiktok")
async def tiktok2(ctx):
      await ctx.respond('Check out the tiktok now! >>> https://tiktok.com/@cjcreatess')

@bot.slash_command(name="verifylink")
async def verifylink2(ctx):
      await ctx.respond('Please link your roblox account >>> https://www.roblox.com/games/11713687819/TDP-Verify')

@bot.slash_command(name="site")
async def site2(ctx):
      await ctx.respond('Check out the website now! >>> https://sites.google.com/view/thedeveloperproject/Home?authuser=0')

@bot.slash_command(name="getroblox")
async def getroblox2(ctx, member: discord.Member):
      key2 = str(member) + '+rbx'
      try:
        await ctx.respond('roblox username = ' + db[key2])
      except:
        await ctx.respond('Failed To Fetch Username')

@bot.slash_command(name="getdiscord")
async def getdiscord2(ctx, username):
      try:
        await ctx.respond('discord username = ' + db[username])
      except:
        await ctx.respond('Failed To Fetch Username')

@bot.slash_command(name="ping")
async def ping2(ctx):
      await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.slash_command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick2(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.kick(member)
    await ctx.respond(f'User {member.mention} has been kicked for {reason}')


@bot.slash_command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban2(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.ban(member)
    await ctx.respond(f'User {member.mention} has been banned for {reason}')

@bot.slash_command(name="verify")
async def verify2(ctx, arg):
    try:
        key = arg + '+temp'
        rname = db[key]
        dname = ctx.author
        db[rname] = str(dname)
        key2 = str(dname) + '+rbx'
        db[key2] = rname
        del db[key]
        await ctx.respond("Successfully Connected to " + rname)
    except Exception as e:
        await ctx.respond(e.message + ' ' + e.args)


@bot.slash_command(name="bubblepopping")
async def bubblepopping2(ctx):
    embed=discord.Embed(title="bubble popping",description="||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||||pop ||")
    await ctx.respond(embed=embed)

@bot.slash_command(name="getprofilepic")
async def gpp(ctx, member: discord.Member):
    await ctx.respond(member.avatar.url)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(939754863301124128)
    embed = discord.Embed(description=f"**{member.mention} left the server**\n\nUser Id: {member.id}", color=0xe74c3c)
    try:
      embed.set_author(name=member, icon_url=member.avatar.url)
    except:
      embed.set_author(name=member)
    await channel.send(embed=embed)

@bot.listen('on_user_update')
async def userlogger(before, after):
    channel = bot.get_channel(939754863301124128)
    if before.avatar != after.avatar and after.avatar is not None:
      embed = discord.Embed(description=f"**{after.mention} changed avatar **\n\n([before])[{before.avatar.url}] **->** ([after])[{after.avatar.url}]\n\nUser Id: {after.id}", color=0xe67e22)
      try:
        embed.set_author(name=after, icon_url=after.avatar.url)
      except:
        embed.set_author(name=after)
      await channel.send(embed=embed)
  
@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel(939754863301124128)
    if before.roles != after.roles and after.roles is not None:
      br = ''
      ar = ''
      for i in before.roles[1:]:
        br = '\n  '.join((br, i.name))
      for i in after.roles[1:]:
        ar = '\n  '.join((ar, i.name))
      embed = discord.Embed(description=f"**{after.mention} roles have changed\n\nRoles Before:**{br}\n\n**Roles After:**{ar}\n\nUser Id: {after.id}", color=0xe67e22)
      try:
        embed.set_author(name=after, icon_url=after.avatar.url)
      except:
        embed.set_author(name=after)
      await channel.send(embed=embed)
      
    if before.nick != after.nick and after.nick is not None:
      embed = discord.Embed(description=f"**{after.mention} changed nickname**\n\n{before.nick} **->** {after.nick}\n\nUser Id: {after.id}", color=0xe67e22)
      try:
        embed.set_author(name=after, icon_url=after.avatar.url)
      except:
        embed.set_author(name=after)
      await channel.send(embed=embed)
      
    if before.avatar != after.avatar and after.avatar is not None:
      embed = discord.Embed(description=f"**{after.mention} changed avatar **\n\n([before])[{before.avatar.url}] **->** ([after])[{after.avatar.url}]\n\nUser Id: {after.id}", color=0xe67e22)
      try:
        embed.set_author(name=after, icon_url=after.avatar.url)
      except:
        embed.set_author(name=after)
      await channel.send(embed=embed)

@bot.event
async def on_thread_create(thread):
    message = await thread.fetch_message(thread.id)
    time.sleep(0.01)
    await message.add_reaction("🔼")
    await message.add_reaction("🔽")

@bot.event
async def on_message(message):
  global cpn, pendingrequests, gpendingrequests
  if message.content and message.content[0] == '+':
    await bot.process_commands(message)
  elif isinstance(message.channel, discord.channel.DMChannel):
    try:
      pendingrequests[message.author.id]
    except:
      try:
        gpendingrequests[message.author.id]
      except:
        pass
      else:
        if message.content == 'cancel':
          del gpendingrequests[message.author.id]
          embed=discord.Embed(title="Request Cancelled!")
          await message.channel.send(embed=embed)
        if gpendingrequests[message.author.id]['point'] == 2:
          gpendingrequests[message.author.id]['point'] = 3
          gpendingrequests[message.author.id]['description'] = message.content
          embed=discord.Embed(title="Describe payment", description="respond with 'cancel' to cancel")
          await message.channel.send(embed=embed)
        elif gpendingrequests[message.author.id]['point'] == 3:
          gpendingrequests[message.author.id]['point'] = 4
          gpendingrequests[message.author.id]['payment'] = message.content
          embed=discord.Embed(title="Post? (Y/n)")
          await message.channel.send(embed=embed)
          pay = gpendingrequests[message.author.id]['payment']
          desc = gpendingrequests[message.author.id]['description']
          dev = gpendingrequests[message.author.id]['dev']
          info = f'**Description:**\n\n{desc}'
          info += f'\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
          try:
            key = message.author.name + '+rbx'
            roblox = db[key]
            info += f'\n\n**Roblox:** {roblox}'
          except:
            pass
          embed=discord.Embed(title=f"{message.author.name}'s Portfolio",description=info)
          embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
          await message.channel.send(embed=embed)
        elif gpendingrequests[message.author.id]['point'] == 4:
          if message.content.lower() == 'y':
            pay = gpendingrequests[message.author.id]['payment']
            desc = gpendingrequests[message.author.id]['description']
            dev = gpendingrequests[message.author.id]['dev']
            info = f'**Description:**\n\n{desc}'
            info += f'\n\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
            try:
              key = message.author.name + '+rbx'
              roblox = db[key]
              info += f'\n\n**Roblox:** {roblox}'
            except:
              pass
            embed=discord.Embed(title=f"{message.author.name}'s Portfolio",description=info)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            channel = bot.get_channel(1049873913628328006 )
            msg = await channel.send(embed=embed)
            del gpendingrequests[message.author.id]
            await msg.add_reaction("🗑️")
            db[str(message.id)] = message.author.id
            embed=discord.Embed(title="sent!")
            await message.author.send(embed=embed)
          elif message.content.lower() == 'n':
            embed=discord.Embed(title="Request Cancelled!")
            await message.channel.send(embed=embed)
            del gpendingrequests[message.author.id]
          else:
            await message.channel.send('Invalid option, please select either "n" for no or "y" for yes.')
    else:
      try:
        if pendingrequests[message.author.id] and message.content == 'cancel':
          del pendingrequests[message.author.id]
          embed=discord.Embed(title="Request Cancelled!")
          await message.channel.send(embed=embed)
        if pendingrequests[message.author.id]['point'] == 2:
          pendingrequests[message.author.id]['point'] = 3
          pendingrequests[message.author.id]['description'] = message.content
          embed=discord.Embed(title="Describe payment", description="respond with 'cancel' to cancel")
          await message.channel.send(embed=embed)
        elif pendingrequests[message.author.id]['point'] == 3:
          pendingrequests[message.author.id]['point'] = 4
          pendingrequests[message.author.id]['payment'] = message.content
          embed=discord.Embed(title="Post? (Y/n)")
          await message.channel.send(embed=embed)
          pay = pendingrequests[message.author.id]['payment']
          desc = pendingrequests[message.author.id]['description']
          dev = pendingrequests[message.author.id]['dev']
          info = f'**Description:**\n\n{desc}'
          info += f'\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
          try:
            key = message.author.name + '+rbx'
            roblox = db[key]
            info += f'\n\n**Roblox:** {roblox}'
          except:
            pass
          embed=discord.Embed(title=f"{message.author.name}'s ticket",description=info)
          embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
          await message.channel.send(embed=embed)
        elif pendingrequests[message.author.id]['point'] == 4:
          if message.content.lower() == 'y':
            pay = pendingrequests[message.author.id]['payment']
            desc = pendingrequests[message.author.id]['description']
            dev = pendingrequests[message.author.id]['dev']
            info = f'**Description:**\n\n{desc}'
            info += f'\n\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
            try:
              key = message.author.name + '+rbx'
              roblox = db[key]
              info += f'\n\n**Roblox:** {roblox}'
            except:
              pass
            embed=discord.Embed(title=f"{message.author.name}'s ticket",description=info)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            channel = bot.get_channel(1055149457886416936 )
            msg = await channel.send(embed=embed)
            del pendingrequests[message.author.id]
            await msg.add_reaction("🗑️")
            db[str(message.id)] = message.author.id
            embed=discord.Embed(title="sent!")
            await message.author.send(embed=embed)
          elif message.content.lower() == 'n':
            embed=discord.Embed(title="Request Cancelled!")
            await message.channel.send(embed=embed)
            del pendingrequests[message.author.id]
          else:
            await message.channel.send('Invalid option, please select either "n" for no or "y" for yes.')

        if gpendingrequests[message.author.id]['point'] == 2:
          print('hello')
          gpendingrequests[message.author.id]['point'] = 3
          gpendingrequests[message.author.id]['description'] = message.content
          embed=discord.Embed(title="Describe payment", description="respond with 'cancel' to cancel")
          await message.channel.send(embed=embed)
        elif gpendingrequests[message.author.id]['point'] == 3:
          gpendingrequests[message.author.id]['point'] = 4
          gpendingrequests[message.author.id]['payment'] = message.content
          embed=discord.Embed(title="Post? (Y/n)")
          await message.channel.send(embed=embed)
          pay = gpendingrequests[message.author.id]['payment']
          desc = gpendingrequests[message.author.id]['description']
          dev = gpendingrequests[message.author.id]['dev']
          info = f'**Description:**\n\n{desc}'
          info += f'\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
          try:
            key = message.author.name + '+rbx'
            roblox = db[key]
            info += f'\n\n**Roblox:** {roblox}'
          except:
            pass
          embed=discord.Embed(title=f"{message.author.name}'s Portfolio",description=info)
          embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
          await message.channel.send(embed=embed)
        elif gpendingrequests[message.author.id]['point'] == 4:
          if message.content.lower() == 'y':
            pay = gpendingrequests[message.author.id]['payment']
            desc = gpendingrequests[message.author.id]['description']
            dev = gpendingrequests[message.author.id]['dev']
            info = f'**Description:**\n\n{desc}'
            info += f'\n\n\n**Developer Type:** {dev}\n\n**Payment:** {pay}\n\n**Contact:** {message.author.mention}'
            try:
              key = message.author.name + '+rbx'
              roblox = db[key]
              info += f'\n\n**Roblox:** {roblox}'
            except:
              pass
            embed=discord.Embed(title=f"{message.author.name}'s Portfolio",description=info)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            channel = bot.get_channel(1054031881953366088)
            msg = await channel.send(embed=embed)
            del gpendingrequests[message.author.id]
            await msg.add_reaction("🗑️")
            db[message.id] = message.author.id
            embed=discord.Embed(title="sent!")
            await message.author.send(embed=embed)
          elif message.content.lower() == 'n':
            embed=discord.Embed(title="Request Cancelled!")
            await message.channel.send(embed=embed)
            del gpendingrequests[message.author.id]
          else:
            await message.channel.send('Invalid option, please select either "n" for no or "y" for yes.')
      except:
        pass
@bot.event
async def on_reaction_add(reaction, user):
  global cpn, gcpn
  if reaction.message.channel == bot.get_channel(1054031881953366088) and not user.bot:
    await reaction.message.remove_reaction("🗑️", user)
    if user.guild_permissions.kick_members or db[str(reaction.message.id)] == user.id:
      del db[str(reaction.message.id)]
      cpn = None
      gcpn = None
      await reaction.message.delete()
      pass

discordkey = os.environ['discordkey']
try:
    bot.run(discordkey)
except:
    os.system("kill 1")
