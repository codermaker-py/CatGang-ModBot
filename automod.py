import discord
from discord.ext import commands
import time
import datetime
import asyncio
from uuid import uuid4
import base64

MOD_LOG =1350425247471636530  #1294290963971178587
AUTOMOD_RULE = "not set"

class AutomodCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.last_executed = 0
    def convert_to_base64(self) ->str:
        u = uuid4()
        return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')
 
    def calc_last_executed(self) ->bool:
        if time.time() - self.last_executed <= 7:
            return False
        self.last_executed = time.time()
        return True
    @commands.Cog.listener("on_message")
    async def message_listener(self, message:discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return
        bucket = self.bot.spam_limit.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after and self.calc_last_executed():
            await self.purge_messages(message.author, message.channel)
            

    async def purge_messages(self, member:discord.Member, channel:discord.TextChannel):
        await asyncio.sleep(3.0)
        def check(msg:discord.Message):
            return msg.author == member and msg.channel == channel
        await channel.purge(limit=15, check=check)
        await channel.send(f"{member.mention} let's avoid spamming!\
                                    \n-# ⚠️ Repeating this can lead into a warning, please read <#1319606464264011806>.", delete_after=5.0)
        await self.warn_user(member)

        
    async def warn_user(self, user: discord.Member | discord.User) -> None:
        async with self.bot.mod_pool.acquire() as conn:
            rows = await conn.execute('''SELECT NULL from moddb WHERE user_id =? AND action = ? ''',
                                         (user.id, "automodwarn"))
            results = await rows.fetchall()
        warns = len(results) + 1 or 0
        action = None
        if warns == 10:
            if isinstance(user, discord.Member) and not user.bot:
                user_embed = discord.Embed(title="You have been autobanned (10 warns)",
                                    description=f">>> **Duration:** Permanent\
                                        \n**Reason:** Spam: `>= 5 messages in 3s`",
                                        timestamp=discord.utils.utcnow(),
                                        color=discord.Color.brand_red())
                
                user_embed.set_author(name=user.guild, icon_url=user.guild.icon.url)
                user_embed.set_thumbnail(url=user.guild.icon.url)
                try:
                    await user.send(embed=user_embed, view=AppealView())
                except discord.Forbidden:
                    pass
            try:
                await user.guild.ban(user, reason=f"AutoBanned for: Spam: `>= 5 messages in 3s`")
            except discord.Forbidden as e:
                print(e)
            except Exception as e:
                await print(f"An error occurred: {e}")
            channel = user.guild.get_channel(MOD_LOG)
            case_id = self.convert_to_base64()
            
            embed = discord.Embed(title=f"Autobanned (`{case_id}`) | 10 warns",
                                description=f">>> **User:** {user.mention} ({user.id})\
                                    \n**Duration:** Permanent\
                                    \n**Reason:** Spam: `>= 5 messages in 3s`",
                                    timestamp=discord.utils.utcnow(),
                                    color=discord.Color.brand_red())
            
            embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=embed)

            action = "ban"
        elif warns == 8:
            if isinstance(user, discord.Member) and not user.bot:
                user_embed = discord.Embed(title="You have been automuted (8 warns)",
                                    description=f">>> **Duration:** 1 day\
                                        \n**Reason:** Spam: `>= 5 messages in 3s`",
                                        timestamp=discord.utils.utcnow(),
                                        color=discord.Color.brand_red())
                
                user_embed.set_author(name=user.guild, icon_url=user.guild.icon.url)
                user_embed.set_thumbnail(url=user.guild.icon.url)
                try:
                    await user.send(embed=user_embed)
                except discord.Forbidden:
                    pass
            try:
                await user.timeout(datetime.timedelta(seconds=1), reason=f"Automuted for: Spam: `>= 5 messages in 3s`")
            except discord.Forbidden as e:
                print(e)
            except Exception as e:
                await print(f"An error occurred: {e}")
            channel = user.guild.get_channel(MOD_LOG)
            case_id = self.convert_to_base64()
            
            embed = discord.Embed(title=f"Automuted (`{case_id}`) | 8 warns",
                                description=f">>> **User:** {user.mention} ({user.id})\
                                    \n**Duration:** 1 day\
                                    \n**Reason:** Spam: `>= 5 messages in 3s`",
                                    timestamp=discord.utils.utcnow(),
                                    color=discord.Color.brand_red())
            
            embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=embed)
            action = "mute"
        elif warns == 5:
            if isinstance(user, discord.Member) and not user.bot:
                user_embed = discord.Embed(title="You have been automuted (5 warns)",
                                    description=f">>> **Duration:** 6 hours\
                                        \n**Reason:** Spam: `>= 5 messages in 3s`",
                                        timestamp=discord.utils.utcnow(),
                                        color=discord.Color.brand_red())
                
                user_embed.set_author(name=user.guild, icon_url=user.guild.icon.url)
                user_embed.set_thumbnail(url=user.guild.icon.url)
                try:
                    await user.send(embed=user_embed)
                except discord.Forbidden:
                    pass
            try:
                await user.timeout(datetime.timedelta(seconds=1), reason=f"Automuted for: Spam: `>= 5 messages in 3s`")
            except discord.Forbidden as e:
                print(e)
            except Exception as e:
                await print(f"An error occurred: {e}")
            channel = user.guild.get_channel(MOD_LOG)
            case_id = self.convert_to_base64()
            embed = discord.Embed(title=f"Automuted (`{case_id}`) | 5 warns",
                    description=f">>> **User:** {user.mention} ({user.id})\
                        \n**Duration:** 6 hours\
                        \n**Reason:** Spam: `>= 5 messages in 3s`",
                        timestamp=discord.utils.utcnow(),
                        color=discord.Color.brand_red())
            
            embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=embed)
            action = "mute"
        elif warns == 2:
            if isinstance(user, discord.Member) and not user.bot:
                user_embed = discord.Embed(title="You have been autowarned (2 warns)",
                                    description=f">>> **Reason:** Spam: `>= 5 messages in 3s`",
                                        timestamp=discord.utils.utcnow(),
                                        color=discord.Color.brand_red())
                
                user_embed.set_author(name=user.guild, icon_url=user.guild.icon.url)
                user_embed.set_thumbnail(url=user.guild.icon.url)
                try:
                    await user.send(embed=user_embed)
                except discord.Forbidden:
                    pass
            channel = user.guild.get_channel(MOD_LOG)
            case_id = self.convert_to_base64()
            
            embed = discord.Embed(title=f"Autowarned (`{case_id}`) | 2 warns",
                                description=f">>> **User:** {user.mention} ({user.id})\
                                    \n**Reason:** Spam: `>= 5 messages in 3s`",
                                    timestamp=discord.utils.utcnow(),
                                    color=discord.Color.brand_red())
            
            embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=embed)
            action = "warn"
        else:
            channel = user.guild.get_channel(MOD_LOG)
            
            embed = discord.Embed(title=f"Automod Spam",
                                description=f">>> **User:** {user.mention} ({user.id})\
                                    \n**Reason:** Spam: `>= 5 messages in 3s`",
                                    timestamp=discord.utils.utcnow(),
                                    color=discord.Color.brand_red())
            
            embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=embed)

        automod_case_id = self.convert_to_base64()
        async with self.bot.mod_pool.acquire() as conn:
            await conn.execute('''INSERT INTO moddb (case_id, user_id, action, mod_id, time) VALUES (?, ?, ?, ?, ?)''',
                                (automod_case_id, user.id, "automodwarn", self.bot.user.id, time.time()))
            if action:
                await conn.execute('''INSERT INTO moddb (case_id, user_id, action, mod_id, time) VALUES (?, ?, ?, ?, ?)''',
                                   (automod_case_id, user.id, action, self.bot.user.id, time.time()))

    @commands.Cog.listener("on_automod_action")
    async def automod_action_listener(self, action:discord.AutoModAction):
        if action.rule_id == : AUTOMOD_RULE
            await action.member.edit(nick="Change nickname to English")



async def setup(bot:commands.Bot):
    await bot.add_cog(AutomodCog(bot))

class AppealView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Appeal", style=discord.ButtonStyle.link, url="https://discord.gg/er2ErWNZjG"))
