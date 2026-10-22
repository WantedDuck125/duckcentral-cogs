import discord
from redbot.core import commands, Config


class GoLive(commands.Cog):
    """Manually announce when you go live on Twitch."""

    DEFAULT_URL = "https://twitch.tv/wantedduck125"
    DEFAULT_TITLE = "🔴 WantedDuck125 is LIVE on Twitch!"
    DEFAULT_MESSAGE = "I'm live on Twitch! Come hang out."

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=874163205771, force_registration=True)
        self.config.register_guild(
            role_id=None,
            channel_id=None,
            twitch_url=self.DEFAULT_URL,
            embed_title=self.DEFAULT_TITLE,
            message_template=self.DEFAULT_MESSAGE,
        )

    async def _get_configured_role(self, guild):
        role_id = await self.config.guild(guild).role_id()
        return guild.get_role(role_id) if role_id else None

    async def _get_configured_channel(self, guild):
        channel_id = await self.config.guild(guild).channel_id()
        channel = guild.get_channel(channel_id) if channel_id else None
        return channel if isinstance(channel, (discord.TextChannel, discord.Thread)) else None

    @commands.command(name="go-live")
    @commands.guild_only()
    async def go_live(self, ctx, *, message: str = None):
        """Post your Twitch go-live embed. Optionally include a custom message."""
        role = await self._get_configured_role(ctx.guild)
        channel = await self._get_configured_channel(ctx.guild)
        twitch_url = await self.config.guild(ctx.guild).twitch_url()
        embed_title = await self.config.guild(ctx.guild).embed_title()
        message_template = await self.config.guild(ctx.guild).message_template()

        missing = []
        if role is None:
            missing.append("announcement role")
        if channel is None:
            missing.append("announcement channel")
        if missing:
            await ctx.send(
                "This cog isn't configured yet. A server admin needs to set the "
                + " and ".join(missing)
                + ". Use `[p]golive setrole @role` and `[p]golive setchannel #channel`."
            )
            return

        announcement_text = message.strip() if message and message.strip() else message_template
        embed = discord.Embed(
            title=embed_title,
            description=announcement_text,
            url=twitch_url,
            color=discord.Color.from_rgb(145, 70, 255),
        )
        embed.add_field(name="Watch here", value=f"[**Watch the stream on Twitch**]({twitch_url})", inline=False)
        embed.set_footer(text="Twitch • Live now")

        allowed_mentions = discord.AllowedMentions(
            everyone=False,
            users=False,
            roles=[role],
            replied_user=False,
        )
        try:
            await channel.send(
                content=role.mention,
                embed=embed,
                allowed_mentions=allowed_mentions,
            )
        except discord.Forbidden:
            await ctx.send(
                "I couldn't post the announcement. Check that I can view and send messages "
                "in the configured channel and that embeds are enabled."
            )
            return
        except discord.HTTPException as exc:
            await ctx.send(f"Discord couldn't send the announcement: {exc}")
            return

        if channel.id != ctx.channel.id:
            await ctx.send(f"Posted your Twitch announcement in {channel.mention}.")
        else:
            await ctx.tick()

    @commands.group(name="golive", invoke_without_command=True)
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def golive(self, ctx):
        """Configure the Twitch go-live announcement."""
        role = await self._get_configured_role(ctx.guild)
        channel = await self._get_configured_channel(ctx.guild)
        twitch_url = await self.config.guild(ctx.guild).twitch_url()
        embed_title = await self.config.guild(ctx.guild).embed_title()
        message_template = await self.config.guild(ctx.guild).message_template()

        role_text = role.mention if role else "Not set"
        channel_text = channel.mention if channel else "Not set"
        embed = discord.Embed(title="Twitch announcement settings", color=discord.Color.blurple())
        embed.add_field(name="Role to ping", value=role_text, inline=False)
        embed.add_field(name="Announcement channel", value=channel_text, inline=False)
        embed.add_field(name="Twitch URL", value=twitch_url, inline=False)
        embed.add_field(name="Embed title", value=embed_title, inline=False)
        embed.add_field(name="Default message", value=message_template, inline=False)
        embed.set_footer(text="Use [p]golive help for configuration commands.")
        await ctx.send(embed=embed)

    @golive.command(name="setrole")
    async def golive_setrole(self, ctx, role: discord.Role):
        """Set the role pinged by [p]go-live."""
        if role.is_default():
            await ctx.send("I can't use @everyone as the configured announcement role.")
            return
        await self.config.guild(ctx.guild).role_id.set(role.id)
        await ctx.send(f"Go-live announcements will ping {role.mention}.")

    @golive.command(name="setchannel")
    async def golive_setchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel where [p]go-live posts."""
        await self.config.guild(ctx.guild).channel_id.set(channel.id)
        await ctx.send(f"Go-live announcements will be posted in {channel.mention}.")

    @golive.command(name="seturl")
    async def golive_seturl(self, ctx, url: str):
        """Set your Twitch channel URL."""
        cleaned = url.strip()
        if not cleaned.startswith(("https://twitch.tv/", "https://www.twitch.tv/")):
            await ctx.send("Please use your Twitch channel URL, for example `https://twitch.tv/yourname`.")
            return
        await self.config.guild(ctx.guild).twitch_url.set(cleaned)
        await ctx.send(f"Twitch URL set to {cleaned}")

    @golive.command(name="settitle")
    async def golive_settitle(self, ctx, *, title: str):
        """Set the title shown on the announcement embed."""
        title = title.strip()
        if not title:
            await ctx.send("The embed title can't be empty.")
            return
        if len(title) > 256:
            await ctx.send("The embed title must be 256 characters or fewer.")
            return
        await self.config.guild(ctx.guild).embed_title.set(title)
        await ctx.send("Go-live embed title updated.")

    @golive.command(name="setmessage")
    async def golive_setmessage(self, ctx, *, message: str):
        """Set the default message used when [p]go-live has no custom text."""
        message = message.strip()
        if not message:
            await ctx.send("The default message can't be empty.")
            return
        if len(message) > 4000:
            await ctx.send("The default message must be 4,000 characters or fewer.")
            return
        await self.config.guild(ctx.guild).message_template.set(message)
        await ctx.send("Default go-live message updated.")

    @golive.command(name="reset")
    async def golive_reset(self, ctx):
        """Reset all go-live settings for this server."""
        await self.config.guild(ctx.guild).clear()
        await ctx.send(
            "Go-live settings reset. Set the role and channel again with "
            "`[p]golive setrole @role` and `[p]golive setchannel #channel`."
        )


async def setup(bot):
    await bot.add_cog(GoLive(bot))
