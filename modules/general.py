import discord, os, importlib, pymongo, re
from discord.ext import commands; from pymongo import MongoClient
import configuration.variables as variables

class FindMember(commands.IDConverter):
    async def convert(self, ctx, argument) -> discord.User:
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        if match == None and ctx.guild:
            result = ctx.guild.get_member_named(argument)
        else:
            userid = int(match.group(1))
            result = ctx.guild.get_member(userid) or await ctx.bot.fetch_user(userid) if ctx.guild else await ctx.bot.fetch_user(userid)
        if result == None:
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        return result

class General(commands.Cog):
    "Simple commands which anybody can use."
    def __init__(self, bot): self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def build(self, ctx): # p!build
        "Shows information regarding the bot."
        embed=discord.Embed(title="Pikachu", url="https://github.com/NoahAbc12345/Pikachu", description="A utility bot for the Nincord server.", color=0xffff00)
        embed.set_author(name="NoahAbc12345 (Maintainer)", icon_url="https://cdn.discordapp.com/avatars/421448353889517579/377a5e8b2e44f3c26e03a905c8c59c14.webp?size=512")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/697972897075036161/b9825ad0c7e74b25f14f2e189c4fff13.webp?size=512")
        embed.set_footer(text=f"Check out my source code on GitHub!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def ping(self, ctx): # p!ping
        "Shows the bot's ping."
        await ctx.send(f"Pong! {round(self.bot.latency*1000)}ms.")

    @commands.command(aliases=["mc"])
    @commands.guild_only()
    async def membercount(self, ctx):
        "Counts the amount of members currently on the server."
        await ctx.send(f"{ctx.guild.name} has {ctx.guild.member_count} members at this moment!")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def invite(self, ctx): # p!invite
        "Shares a link to the Nincord server."
        await ctx.send(f"{ctx.author.mention}, share this link to invite people to Nincord! https://discord.gg/mYjeaZQ")

    @commands.command(aliases=["ui"])
    @commands.guild_only()
    async def userinfo(self, ctx, user: FindMember = None): # p!userinfo
        "Displays information regarding a user's account. Staff members can use this command on others."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerRole in ctx.author.roles or modRole in ctx.author.roles or botRole in ctx.author.roles:
            if user == None: user = ctx.author
            if isinstance(user, discord.Member):
                role = user.top_role.name
                embed=discord.Embed(title=user.display_name, description=role, color=0xffff00)
            else:
                embed=discord.Embed(title=user.display_name, color=0xffff00)
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
            embed.add_field(name="Account Name:", value=user.name, inline=True)
            embed.add_field(name="Discriminator:", value="#"+user.discriminator, inline=True)
            embed.add_field(name="Account Identification:", value=user.id, inline=False)
            formatCreate = user.created_at
            formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
            if isinstance(user, discord.Member): formatJoin = user.joined_at
            if isinstance(user, discord.Member): formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
            embed.add_field(name="Created:", value="{}".format(formatCreate2), inline=False)
            if isinstance(user, discord.Member): embed.add_field(name="Joined:", value="{}".format(formatJoin2), inline=False)
            if collection.count_documents({"_id": user.id}, limit = 1) != 0:
                results = collection.find({"_id": user.id})
                for result in results:
                    checkWarn1 = result["Warn 1"]
                    checkWarn2 = result["Warn 2"]
                    checkWarn3 = result["Warn 3"]
                if checkWarn3 != None: warns = "3"
                elif checkWarn3 == None and checkWarn2 != None: warns = "2"
                elif checkWarn2 == None and checkWarn1 != None: warns = "1"
                embed.add_field(name="Warns:", value=warns, inline=True)
            else:
                embed.add_field(name="Warns:", value="0", inline=True)
            if not isinstance(user, discord.Member):
                try:
                    banned = await ctx.guild.fetch_ban(user)
                    embed.add_field(name="Banned:", value=f"{banned.reason}", inline=False)
                except discord.NotFound:
                    banned = None
                    # embed.add_field(name="Banned:", value="N/A", inline=False)
            await ctx.send(embed=embed)
        else: # Another example of bad Python coding. I plan to simplify it later on, but at least it works for now.
            if user != None: await ctx.send(f"{ctx.author.mention}, only staff members can use this command on others.")
            else:
                if user == None: user = ctx.author
                if isinstance(user, discord.Member):
                    role = user.top_role.name
                    embed=discord.Embed(title=user.display_name, description=role, color=0xffff00)
                else: embed=discord.Embed(title=user.display_name, color=0xffff00)
                embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
                embed.add_field(name="Account Name:", value=user.name, inline=True)
                embed.add_field(name="Discriminator:", value="#"+user.discriminator, inline=False)
                embed.add_field(name="Account Identification:", value=user.id, inline=False)
                formatCreate = user.created_at
                formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
                if isinstance(user, discord.Member): formatJoin = user.joined_at
                if isinstance(user, discord.Member): formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
                embed.add_field(name="Created:", value="{}".format(formatCreate2), inline=False)
                if isinstance(user, discord.Member): embed.add_field(name="Joined:", value="{}".format(formatJoin2), inline=False)
                if collection.count_documents({"_id": user.id}, limit = 1) != 0:
                    results = collection.find({"_id": user.id})
                    for result in results:
                        checkWarn1 = result["Warn 1"]
                        checkWarn2 = result["Warn 2"]
                        checkWarn3 = result["Warn 3"]
                    if checkWarn3 != None: warns = "3"
                    elif checkWarn3 == None and checkWarn2 != None: warns = "2"
                    elif checkWarn2 == None and checkWarn1 != None: warns = "1"
                    embed.add_field(name="Warns:", value=warns, inline=False)
                else: embed.add_field(name="Warns:", value="0", inline=False)
                if not isinstance(user, discord.Member):
                    try:
                        banned = await ctx.guild.fetch_ban(user)
                        embed.add_field(name="Banned:", value=f"{banned.reason}", inline=False)
                    except discord.NotFound:
                        banned = None
                        # embed.add_field(name="Banned:", value="N/A", inline=False)
                await ctx.send(embed=embed)

    @commands.command(aliases=["si"])
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def serverinfo(self, ctx): # p!serverinfo
        "Displays information regarding a server."
        embed = discord.Embed(title=ctx.guild.name, color=0xffff00)
        embed.add_field(name="Server Identification:", value=ctx.guild.id, inline=False)
        embed.add_field(name="Server Owner:", value=ctx.guild.owner, inline=True)
        servercreate = ctx.guild.created_at
        servercreate2 = servercreate.strftime("%B %d, %Y (%I:%M %p)")
        embed.add_field(name="Created:", value="{}".format(servercreate2), inline=False)
        embed.add_field(name="Members:", value= ctx.guild.member_count)
        embed.add_field(name="Role Count:", value=len(ctx.guild.roles), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png"))
        await ctx.send(embed=embed)

    @commands.command(aliases=["stafflist"])
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def liststaff(self, ctx):
        modRole = ctx.guild.get_role(variables.SERVERMODERATOR)
        description = []
        for member in modRole.members:
            description.append(f"\n {member.mention}")
        embed = discord.Embed(title=f"{ctx.guild.name} Staff Team", description="".join(description), color=0xffff40)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def suggest(self, ctx, *, idea): # p!suggest
        "Suggest something which could be changed or added to the server."
        requestLog = self.bot.get_channel(variables.REQUESTLOGS) # Channel #request-logs.
        embed=discord.Embed(color=0x8080ff)
        embed.add_field(name="Suggestion:", value=f"{idea}", inline=False)
        suggestion = await requestLog.send(f"{ctx.author} ({ctx.author.id}) has submitted a suggestion for the server.", embed=embed)
        await suggestion.add_reaction("\U0001F44D")
        await suggestion.add_reaction("\U0001F44E")
        await ctx.send(f"{ctx.author.mention}, your suggestion has successfully been submitted. It will be reviewed internally.")

def setup(bot): bot.add_cog(General(bot))
