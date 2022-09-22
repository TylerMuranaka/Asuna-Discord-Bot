import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
from discord.ext.commands import Paginator 
import os



TOKEN = "Nzg4MjUyMTI0NTA0OTE1OTY4.X9gy_w.ZYRxIbSRYJmrhZKgjXPe384qLz4"
intents = discord.Intents.all()
intents.members = True 
client = commands.Bot(command_prefix="!", guild_subscriptions = True, intents=intents)



@client.event
async def on_ready():
    print("Asuna is now ready!")
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('SAO!'))



@client.event
async def on_member_remove(member):
    print(f"""{member.mention} has left the server""")



@client.command()
async def hello(ctx):
    await ctx.send("hello " + str(ctx.author.mention) + ", my name is Asuna.")



@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is at {round(client.latency * 1000)}ms, now dont forget silly.')



@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount) 



@client.command()
@commands.has_guild_permissions(manage_guild=True)
async def setdelay(ctx, seconds:int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"I have slowed you idiots down to **{seconds}** seconds!")



@client.command(aliases=["k"])
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user is None:
        em = discord.Embed(color=discord.Color.red())
        em.add_field(name="Isufficient Values", value="thx for using Asuna if you find any bug plz report using `!report<bug here>`")
        await ctx.send(embed=em)
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        em1 = discord.Embed(color=discord.Color.red())
        em1.add_field(name = "You cannot kick this user because their role is higher than or equal to yours silly." , value = "")
        await ctx.send(embed = em1)
    else:
        await ctx.guild.kick(user, reason=reason)
        if reason:
            await ctx.send(f"User **{user}** has been kicked for reason: **{reason}**.")
        else:
            em2 = discord.Embed(color=discord.Color.green())
            em2.add_field(name = f"User **{user}** has been kicked." , value = "Thank you for using Asuna!")
            await ctx.send(embed = em2)

            em3 = discord.Embed(color=discord.Color.blurple())
            em3.add_field(name =f"You have been **kicked** from **{ctx.guild}** server due to the following reason:\n**{reason}**" , value = "BAHAHA, next time dont be so rude." )
            await user.send(embed = em3)



@client.command(aliases=["b"])
@commands.has_permissions(manage_roles=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban()
    await ctx.send(f"BAHAHA, that punk has been banned!")



@client.command(aliases=["ub"])
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return



@client.command(aliases=["g"])
async def guilds(ctx):  
    for guild in client.guilds:
        em = discord.Embed(title=str(guild), color=discord.Color.dark_gold())
        em.set_thumbnail(url=guild.icon_url)
        em.add_field(name="Owner:", value=guild.owner, inline=False)
        em.add_field(name="Members:", value=guild.member_count, inline=False)
        await ctx.send(embed=em)



@client.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]

    em = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    em.set_author(name=f"User Info - {member}")
    em.set_thumbnail(url=member.avatar_url)
    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    em.add_field(name="ID", value=member.id)
    em.add_field(name="Guild Name", value=member.display_name)

    em.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")) 
    em.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    em.add_field(name="Top Role:", value=member.top_role.mention)

    await ctx.send(embed=em)
"""
*Games
"""
@client.command(aliases=["c"], pass_context=True)
async def coinflip(ctx):
    coins = ["Heads", "Tails"]
    random_coins = random.choice(coins)
    await ctx.send(random_coins)
    await ctx.send(f"That was fun lets do it again!")



cogsx=['music']
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            raise e


            
client.run(TOKEN)