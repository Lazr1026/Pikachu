import discord, os, importlib, pymongo, re, typing
from discord.ext import commands; from pymongo import MongoClient; from subprocess import check_output
from manager import is_staff_member, check_staff_member
import configuration.variables as variables
import configuration.arrays as arrays

class General(commands.Cog):
    "Simple commands which anybody can use."
    def __init__(self, bot): self.bot = bot
        
    @commands.command(aliases=["about", "info", "version"])
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def build(self, ctx): # p!build
        "Shows information regarding the bot."
        commit = os.environ.get("COMMIT_SHA", "Unknown")
        branch = os.environ.get("COMMIT_BRANCH", "Unknown")
        if commit == "Unknown" or branch == "Unknown":
            try:
                commit = check_output(["git", "rev-parse", "HEAD"]).decode("ascii")[:-1]
                branch = check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode()[:-1]
            except: commit = "Unknown"; branch = "Unknown"
        if commit == "Unknown" or branch == "Unknown":
            try: commit = variables.HEROKUCOMMIT; branch = "master"
            except: commit = "Unknown"; branch = "Unknown"
        embed=discord.Embed(title="Pikachu", url="https://github.com/NoahAbc12345/Pikachu", description="A utility bot for the Nincord server.", color=0xffff00)
        embed.set_author(name="NoahAbc12345 (Maintainer)", icon_url="https://avatars3.githubusercontent.com/u/63483138?s=460&u=2efd374ab56a340cc3f9e8dd5aa359307a9d1523&v=4")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/697972897075036161/b9825ad0c7e74b25f14f2e189c4fff13.webp?size=512")
        embed.add_field(name="Branch", value=branch, inline=True)
        if commit != "Unknown": embed.add_field(name="Commit", value=commit[0:7], inline=True)
        else: embed.add_field(name="Commit", value=commit, inline=True)
        embed.set_footer(text=f"Check out my source code on GitHub!")
        await ctx.send(f"{ctx.author.mention}, here's some information about me!", embed=embed)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def ping(self, ctx): # p!ping
        "Shows the bot's ping on the network."
        await ctx.send(f"{ctx.author.mention}, pong! {round(self.bot.latency*1000)}ms.")

    @commands.command(aliases=["mc"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def membercount(self, ctx):
        "Counts the amount of members currently on the server."
        await ctx.send(f"{ctx.guild.name} has {ctx.guild.member_count} members at this moment!")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def invite(self, ctx, server = None): # p!invite
        "Shares a link to an invite for this server and affiliated servers.\nServers include \"apple\" and \"resistance\"."
        if server != None: code = arrays.INVITECODES.get(server.capitalize())
        if server == None or code == None: server = "Nincord"; code = arrays.INVITECODES.get(server.capitalize())
        if server.capitalize() == "Nincord": await ctx.send(f"{ctx.author.mention}, share this link to invite people to our server! https://discord.gg/{code}")
        else: await ctx.send(f"{ctx.author.mention}, here is the link for the affiliated server you requested! https://discord.gg/{code}")

    @commands.command(aliases=["ui"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def userinfo(self, ctx, user: typing.Union[discord.Member, discord.User, int] = None): # p!userinfo
        "Displays information regarding a user's account.\nStaff members can use this command on others."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if isinstance(user, (discord.User, int)): user = await self.bot.fetch_user(user)
        async def showUserProfile(user):
            if isinstance(user, discord.Member):
                role = user.top_role.name
                embed=discord.Embed(title=user.display_name, description=role, color=0xffff00)
            else: embed=discord.Embed(title=user.display_name, color=0xffff00)
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
            embed.add_field(name="Account Name", value=user.name, inline=True)
            embed.add_field(name="Discriminator", value="#"+user.discriminator, inline=False)
            embed.add_field(name="Account Identification", value=user.id, inline=False)
            formatCreate = user.created_at
            formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
            if isinstance(user, discord.Member): formatJoin = user.joined_at
            if isinstance(user, discord.Member): formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
            embed.add_field(name="Created", value="{}".format(formatCreate2), inline=False)
            if isinstance(user, discord.Member):
                embed.add_field(name="Joined", value="{}".format(formatJoin2), inline=False)
            if not check_staff_member(user):
                if collection.count_documents({"_id": user.id}, limit = 1) != 0:
                    results = collection.find({"_id": user.id})
                    for result in results:
                        checkWarn1 = result["Warn 1"]
                        checkWarn2 = result["Warn 2"]
                        checkWarn3 = result["Warn 3"]
                    if checkWarn3 != None: warns = "3"
                    elif checkWarn3 == None and checkWarn2 != None: warns = "2"
                    elif checkWarn2 == None and checkWarn1 != None: warns = "1"
                    embed.add_field(name="Warns", value=warns, inline=False)
                else: embed.add_field(name="Warns", value="0", inline=False)
            if not isinstance(user, discord.Member):
                try:
                    banned = await ctx.guild.fetch_ban(user)
                    embed.add_field(name="Banned", value=f"{banned.reason}", inline=False)
                except discord.NotFound: banned = None
            if user == ctx.author: await ctx.send(f"{ctx.author.mention}, here's some information about you.", embed=embed)
            else: await ctx.send(f"{ctx.author.mention}, here's some information about {user.mention}.", embed=embed)
        if check_staff_member(ctx.author):
            if user == None: user = ctx.author
            return await showUserProfile(user)
        if user != ctx.author and user != None:
            return await ctx.send(f"{ctx.author.mention}, using this command on others is only allowed for staff members.")
        user = ctx.author; return await showUserProfile(user)

    @commands.command(aliases=["si"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def serverinfo(self, ctx): # p!serverinfo
        "Displays information regarding the server, such as role count."
        embed = discord.Embed(title=ctx.guild.name, color=0xffff00)
        embed.add_field(name="Server Owner", value=ctx.guild.owner.mention, inline=False)
        embed.add_field(name="Server Identification", value=ctx.guild.id, inline=True)
        servercreate = ctx.guild.created_at
        servercreate2 = servercreate.strftime("%B %d, %Y (%I:%M %p)")
        embed.add_field(name="Created", value="{}".format(servercreate2), inline=False)
        embed.add_field(name="Members", value= ctx.guild.member_count)
        embed.add_field(name="Role Count", value=len(ctx.guild.roles), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png"))
        await ctx.send(f"{ctx.author.mention}, here's some information about the server.", embed=embed)

    @commands.command(aliases=["stafflist"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def liststaff(self, ctx): # p!liststaff
        "Lists the current staff team members on the server."
        staffList = []; dupeChecker = []
        for role in arrays.ROLEINFORMATION:
            if role != variables.SERVERBOT:
                info = arrays.ROLEINFORMATION.get(role)
                staffSetting = info.get("Staff")
                if staffSetting:
                    staffRole = discord.utils.get(ctx.guild.roles, id=role)
                    for member in staffRole.members: dupeChecker.append(f"{member.mention}")
        for user in dupeChecker: 
            if user not in staffList: staffList.append(user)
        embed = discord.Embed(title=f"{ctx.guild.name} Staff Team", description="\n".join(staffList), color=0xffff40)
        await ctx.send(f"{ctx.author.mention}, here's the staff team of {ctx.guild.name}.", embed=embed)

    @commands.command(aliases=["togglerole", "role"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def roletoggle(self, ctx, role): # p!roletoggle
        "Grants a user the specified role.\nValid options are \"gamenight\" for \"@Game Night Player\"."
        for dictionary in arrays.ROLEINFORMATION:
            info = arrays.ROLEINFORMATION.get(dictionary)
            nick = info.get("Nick")
            if nick.lower() == role.lower():
                public = info.get("Public")
                if not public: break
                role = discord.utils.get(ctx.guild.roles, id=dictionary)
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
                    return await ctx.send(f"{ctx.author.mention}, you have lost the <@&{role.id}> role.")
                else:
                    await ctx.author.add_roles(role)
                    return await ctx.send(f"{ctx.author.mention}, you have gained the <@&{role.id}> role.")
        await ctx.send(f"{ctx.author.mention}, this is not a valid togglable role.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def suggest(self, ctx, *, idea): # p!suggest
        "Suggest something which could be changed or added to the server."
        requestLog = self.bot.get_channel(variables.REQUESTLOGS) # Channel #request-logs.
        embed=discord.Embed(color=0x8080ff)
        embed.add_field(name="Suggestion", value=f"{idea}", inline=False)
        suggestion = await requestLog.send(f"{ctx.author.mention} ({ctx.author.id}) has submitted a suggestion for the server.", embed=embed)
        await suggestion.add_reaction("\U0001F44D")
        await suggestion.add_reaction("\U0001F44E")
        await ctx.send(f"{ctx.author.mention}, your suggestion has successfully been submitted. It will be reviewed internally.")

def setup(bot): bot.add_cog(General(bot))
