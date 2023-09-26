import random
import typing

import discord

from discord import app_commands
from discord.ext import commands

from discord.app_commands import Choice

import utils


class Find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self):
        return
        # use for later.

    @app_commands.command(description="Find a new song to listen to", name="find")
    async def find_song(
        self,
        interaction: discord.Interaction,
        user : typing.Optional[typing.Union[discord.Member, discord.User]],
        service : typing.Optional[str],
    ):
        
        cur = await self.bot.db.cursor()

        if user and not service:
            
            user_id = user.id

            result = await cur.execute("SELECT user_id from data WHERE user_id = ?", user)

            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            name = f"User Songs"
            value = f"{user}"


        if service and not user:
            result = await cur.execute("SELECT url from data WHERE service = ?", service)
            
            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            name = "Service Songs"
            value = f"{url.Service}"

        if service and user:

            user = user.id

            result = await cur.execute("SELECT url from data WHERE service = ? and user_id = ?", service, user_id)
            
            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            name = "User and Service Songs"
            value = f"{user}"  

        embed = discord.Embed(title="Random Song", description=f"Service:\n{url.Service} \nAdded By: \n{user}")

        embed.add_field(name=name, value=value)

        await interaction.response.send_message(embed=embed)


    @find_song.autocomplete('service')
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        services = self.bot.services
        
        all_choices = [Choice(name=service.Service, value=service.Service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith


async def setup(bot):
    await bot.add_cog(Find(bot))