"""MIT License.

Copyright (c) 2020-2021 Faholan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import typing as t
from datetime import datetime
from random import choice

import discord
from discord.ext import commands, tasks


class Pic:
    """Picture placeholder."""

    def __init__(self, url: str, tag: str = discord.Embed.Empty) -> None:
        """Create the Pic."""
        self.url = url
        self.title = tag


class Animals(commands.Cog):
    """Get cute pics of animals."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize Animals."""
        self.bot = bot
        self.all_facts: t.List[t.Dict[str, str]] = []
        self.catfact_update.start()

    @tasks.loop(hours=12)
    async def catfact_update(self) -> None:
        """Update the catfacts."""
        url = "https://cat-fact.herokuapp.com/facts"
        async with self.bot.aio_session.get(url) as response:
            self.all_facts = await response.json()

    @commands.command()
    async def catfact(self, ctx: commands.Context) -> None:
        """Send a random cat fact."""
        fact = choice(self.all_facts)
        await ctx.send(fact["text"])

    @commands.command()
    async def fox(self, ctx: commands.Context) -> None:
        """Send a random fox picture."""
        url = "https://randomfox.ca/floof/"
        async with self.bot.aio_session.get(url) as response:
            picture = await response.json()

            embed = discord.Embed(
                timestamp=datetime.utcnow(),
                colour=discord.Colour.blue(),
            )
            embed.set_image(url=picture["image"])
            await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the Animals cog."""
    bot.add_cog(Animals(bot))
