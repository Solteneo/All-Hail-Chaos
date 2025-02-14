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

import asyncio
import typing as t
from datetime import datetime

import discord
from discord.ext import commands, menus
from discord.utils import find

auto_swear_detection = frozenset({
    "4r5e",
    "5h1t",
    "5hit",
    "a55",
    "anal",
    "anus",
    "ar5e",
    "arrse",
    "arse",
    "ass",
    "ass-fucker",
    "asses",
    "assfucker",
    "assfukka",
    "asshole",
    "assholes",
    "asswhole",
    "a_s_s",
    "b!tch",
    "b00bs",
    "b17ch",
    "b1tch",
    "ballbag",
    "balls",
    "ballsack",
    "bastard",
    "beastial",
    "beastiality",
    "bellend",
    "bestial",
    "bestiality",
    "bi+ch",
    "biatch",
    "bitch",
    "bitcher",
    "bitchers",
    "bitches",
    "bitchin",
    "bitching",
    "bloody",
    "blow job",
    "blowjob",
    "blowjobs",
    "boiolas",
    "bollock",
    "bollok",
    "boner",
    "boob",
    "boobs",
    "booobs",
    "boooobs",
    "booooobs",
    "booooooobs",
    "breasts",
    "buceta",
    "bugger",
    "bum",
    "bunny fucker",
    "butt",
    "butthole",
    "buttmuch",
    "buttplug",
    "c0ck",
    "c0cksucker",
    "carpet muncher",
    "cawk",
    "chink",
    "cipa",
    "cl1t",
    "clit",
    "clitoris",
    "clits",
    "cnut",
    "cock",
    "cock-sucker",
    "cockface",
    "cockhead",
    "cockmunch",
    "cockmuncher",
    "cocks",
    "cocksuck",
    "cocksucked",
    "cocksucker",
    "cocksucking",
    "cocksucks",
    "cocksuka",
    "cocksukka",
    "cok",
    "cokmuncher",
    "coksucka",
    "coon",
    "cox",
    "crap",
    "cum",
    "cummer",
    "cumming",
    "cums",
    "cumshot",
    "cunilingus",
    "cunillingus",
    "cunnilingus",
    "cunt",
    "cuntlick",
    "cuntlicker",
    "cuntlicking",
    "cunts",
    "cyalis",
    "cyberfuc",
    "cyberfuck",
    "cyberfucked",
    "cyberfucker",
    "cyberfuckers",
    "cyberfucking",
    "d1ck",
    "damn",
    "dick",
    "dickhead",
    "dildo",
    "dildos",
    "dink",
    "dinks",
    "dirsa",
    "dlck",
    "dog-fucker",
    "doggin",
    "dogging",
    "donkeyribber",
    "doosh",
    "duche",
    "dyke",
    "ejaculate",
    "ejaculated",
    "ejaculates",
    "ejaculating",
    "ejaculatings",
    "ejaculation",
    "ejakulate",
    "f u c k",
    "f u c k e r",
    "f4nny",
    "fag",
    "fagging",
    "faggitt",
    "faggot",
    "faggs",
    "fagot",
    "fagots",
    "fags",
    "fanny",
    "fannyflaps",
    "fannyfucker",
    "fanyy",
    "fatass",
    "fcuk",
    "fcuker",
    "fcuking",
    "feck",
    "fecker",
    "felching",
    "fellate",
    "fellatio",
    "fingerfuck",
    "fingerfucked",
    "fingerfucker",
    "fingerfuckers",
    "fingerfucking",
    "fingerfucks",
    "fistfuck",
    "fistfucked",
    "fistfucker",
    "fistfuckers",
    "fistfucking",
    "fistfuckings",
    "fistfucks",
    "flange",
    "fook",
    "fooker",
    "fuck",
    "fucka",
    "fucked",
    "fucker",
    "fuckers",
    "fuckhead",
    "fuckheads",
    "fuckin",
    "fucking",
    "fuckings",
    "fuckingshitmotherfucker",
    "fuckme",
    "fucks",
    "fuckwhit",
    "fuckwit",
    "fudge packer",
    "fudgepacker",
    "fuk",
    "fuker",
    "fukker",
    "fukkin",
    "fuks",
    "fukwhit",
    "fukwit",
    "fux",
    "fux0r",
    "f_u_c_k",
    "gangbang",
    "gangbanged",
    "gangbangs",
    "gaylord",
    "gaysex",
    "goatse",
    "God",
    "god-dam",
    "god-damned",
    "goddamn",
    "goddamned",
    "hardcoresex",
    "hell",
    "heshe",
    "hoar",
    "hoare",
    "hoer",
    "homo",
    "hore",
    "horniest",
    "horny",
    "hotsex",
    "jack-off",
    "jackoff",
    "jap",
    "jerk-off",
    "jism",
    "jiz",
    "jizm",
    "jizz",
    "kawk",
    "knob",
    "knobead",
    "knobed",
    "knobend",
    "knobhead",
    "knobjocky",
    "knobjokey",
    "kock",
    "kondum",
    "kondums",
    "kum",
    "kummer",
    "kumming",
    "kums",
    "kunilingus",
    "l3i+ch",
    "l3itch",
    "labia",
    "lmfao",
    "lust",
    "lusting",
    "m0f0",
    "m0fo",
    "m45terbate",
    "ma5terb8",
    "ma5terbate",
    "masochist",
    "master-bate",
    "masterb8",
    "masterbat*",
    "masterbat3",
    "masterbate",
    "masterbation",
    "masterbations",
    "masturbate",
    "mo-fo",
    "mof0",
    "mofo",
    "mothafuck",
    "mothafucka",
    "mothafuckas",
    "mothafuckaz",
    "mothafucked",
    "mothafucker",
    "mothafuckers",
    "mothafuckin",
    "mothafucking",
    "mothafuckings",
    "mothafucks",
    "mother fucker",
    "motherfuck",
    "motherfucked",
    "motherfucker",
    "motherfuckers",
    "motherfuckin",
    "motherfucking",
    "motherfuckings",
    "motherfuckka",
    "motherfucks",
    "muff",
    "mutha",
    "muthafecker",
    "muthafuckker",
    "muther",
    "mutherfucker",
    "n1gga",
    "n1gger",
    "nazi",
    "nigg3r",
    "nigg4h",
    "nigga",
    "niggah",
    "niggas",
    "niggaz",
    "nigger",
    "niggers",
    "nob",
    "nob jokey",
    "nobhead",
    "nobjocky",
    "nobjokey",
    "numbnuts",
    "nutsack",
    "orgasim",
    "orgasims",
    "orgasm",
    "orgasms",
    "p0rn",
    "pawn",
    "pecker",
    "penis",
    "penisfucker",
    "phonesex",
    "phuck",
    "phuk",
    "phuked",
    "phuking",
    "phukked",
    "phukking",
    "phuks",
    "phuq",
    "pigfucker",
    "pimpis",
    "piss",
    "pissed",
    "pisser",
    "pissers",
    "pisses",
    "pissflaps",
    "pissin",
    "pissing",
    "pissoff",
    "poop",
    "porn",
    "porno",
    "pornography",
    "pornos",
    "prick",
    "pricks",
    "pron",
    "pube",
    "pusse",
    "pussi",
    "pussies",
    "pussy",
    "pussys",
    "rectum",
    "retard",
    "rimjaw",
    "rimming",
    "s hit",
    "s.o.b.",
    "sadist",
    "schlong",
    "screwing",
    "scroat",
    "scrote",
    "scrotum",
    "semen",
    "sex",
    "sh!+",
    "sh!t",
    "sh1t",
    "shag",
    "shagger",
    "shaggin",
    "shagging",
    "shemale",
    "shi+",
    "shit",
    "shitdick",
    "shite",
    "shited",
    "shitey",
    "shitfuck",
    "shitfull",
    "shithead",
    "shiting",
    "shitings",
    "shits",
    "shitted",
    "shitter",
    "shitters",
    "shitting",
    "shittings",
    "shitty",
    "skank",
    "slut",
    "sluts",
    "smegma",
    "smut",
    "snatch",
    "son-of-a-bitch",
    "spac",
    "spunk",
    "s_h_i_t",
    "t1tt1e5",
    "t1tties",
    "teets",
    "teez",
    "testical",
    "testicle",
    "tit",
    "titfuck",
    "tits",
    "titt",
    "tittie5",
    "tittiefucker",
    "titties",
    "tittyfuck",
    "tittywank",
    "titwank",
    "tosser",
    "turd",
    "tw4t",
    "twat",
    "twathead",
    "twatty",
    "twunt",
    "twunter",
    "v14gra",
    "v1gra",
    "vagina",
    "viagra",
    "vulva",
    "w00se",
    "wang",
    "wank",
    "wanker",
    "wanky",
    "whoar",
    "whore",
    "willies",
    "willy",
    "xrated",
    "xxx",
})


class RoleSource(menus.ListPageSource):
    """Source for the role rule list."""

    def __init__(self, contents: t.List[str], guild_name: str,
                 del_msg: str) -> None:
        """Initialize RoleSource."""
        self.guild_name = guild_name
        self.del_msg = del_msg
        super().__init__(contents, per_page=1)

    async def format_page(
        self,
        menu: menus.Menu,
        page: str,
    ) -> discord.Embed:
        """Create the embed."""
        embed = discord.Embed(
            title=f"Rules for guild {self.guild_name}",
            colour=discord.Colour.blue(),
            description=("You need the rule number for the `remove` action."
                         f"{self.del_msg}\n\n{page}"),
        )
        embed.set_footer(
            text=f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed


class Moderation(commands.Cog):
    """Manage your server like never before."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize Moderation."""
        self.bot = bot
        self._role_add: t.Any = None
        self._role_add_lock: t.Any = None
        self._role_remove: t.Any = None
        self._role_remove_lock: t.Any = None
        self._role_save: t.Any = None
        self._role_save_lock: t.Any = None
        self._swear_conn: t.Any = None
        self._swear_conn_lock: t.Any = None

    @commands.command()
    async def reputation(
        self,
        ctx: commands.Context,
        *,
        other: t.Union[discord.Member, int],
    ) -> None:
        """Check the reputation of an user.

        You can refer to him if he's in the same server, or just paste his ID
        """
        if not self.bot.discord_rep:
            await ctx.send(
                "Sorry, but my owner hasn't correctly configured this command")
            return
        if isinstance(other, int):
            user_id = str(other)
            name = f"User {user_id}"
            url = ctx.bot.user.avatar_url
        else:
            user_id = str(other.id)
            name = f"{other} [{user_id}]"
            url = other.avatar_url

        async with self.bot.aio_session.get(
                f"https://discordrep.com/u/{user_id}") as response:
            if response.status != 200:
                await self.bot.httpcat(
                    ctx,
                    404,
                    "I couldn't find this user.",
                )
                return

        async with self.bot.aio_session.get(
                f"https://discordrep.com/api/v3/rep/{user_id}",
                headers={"Authorization": self.bot.discord_rep},
        ) as response:
            reputation = await response.json()

        async with self.bot.aio_session.get(
                f"https://discordrep.com/api/v3/infractions/{user_id}",
                headers={"Authorization": self.bot.discord_rep},
        ) as response:
            infractions = await response.json()

        embed = discord.Embed(
            colour=discord.Colour.dark_green(),
            description=("Source : [DiscordRep](https://discordrep.com)"),
        )
        embed.set_thumbnail(url=url)
        embed.set_author(name=name,
                         icon_url=url,
                         url=f"https://discordrep.com/u/{user_id}")
        banning: t.List[str] = []
        if infractions.get("type") == "BAN":
            date = datetime.fromtimestamp(infractions["date"] // 1000)
            embed.colour = 0xFFFF00
            banning.append(
                f"Warned on {date.day}-{date.month}-{date.year} "
                f"{date.hour}:{date.minute}:{date.second} because of : "
                f"`{infractions['reason']}`")
        elif infractions.get("type") == "WARN":
            date = datetime.fromtimestamp(infractions["date"] // 1000)
            embed.colour = discord.Colour.red()
            banning.append(
                f"Banned on {date.day}-{date.month}-{date.year} "
                f"{date.hour}:{date.minute}:{date.second} because of : "
                f"`{infractions['reason']}`")
        if banning == []:
            embed.add_field(
                name="Bans",
                value="This user hasn't been banned from DiscordRep",
                inline=False,
            )
        else:
            embed.add_field(
                name="Bans from DiscordRep",
                value="\n".join(banning),
            )

        embed.add_field(
            name="Reputation on DiscordRep",
            value=(f"Rank : {reputation['rank']}\n\nUpvotes : "
                   f"{reputation['upvotes']}\nDownvotes : "
                   f"{reputation['downvotes']}\n\nTotal votes : "
                   f"{reputation['upvotes']-reputation['downvotes']}\n\nXP : "
                   f"{reputation['xp']}"),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.group(aliases=["roles"],
                    invoke_without_command=True,
                    case_insensitive=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx: commands.Context) -> None:
        """Automatically gives a role to anyone who reacts to a message.

        We both need the `manage_roles` permission for that.
        """
        await ctx.send_help("role")

    @role.command()
    async def add(
        self,
        ctx: commands.Context,
        roles: commands.Greedy[discord.Role],
    ) -> None:
        """Add a new rule for this server."""
        async with self.bot.pool.acquire() as database:
            if not roles:
                await ctx.send(
                    "Ping one or more roles in the next 30 seconds to "
                    "select which ones you want to add")

                def check(message: discord.Message) -> bool:
                    """Check the answer."""
                    return message.channel == ctx.channel and (
                        bool(message.role_mentions)
                        and message.author == ctx.author)

                try:
                    message = await self.bot.wait_for(
                        "message",
                        check=check,
                        timeout=30,
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        "You didn't answer in time, I'm giving up on this")
                    return

                roles = message.role_mentions

            await ctx.send(
                "React with an emoji in the next 30 seconds to a message to set up the assignation !"
            )

            def check2(payload: discord.RawReactionActionEvent) -> bool:
                """Check the reaction."""
                return payload.guild_id == ctx.guild.id and (payload.member
                                                             == ctx.author)

            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add",
                    check=check2,
                    timeout=30,
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    "You didn't react in time, I'm giving up on this.")
                return

            message = await self.bot.get_channel(
                payload.channel_id).fetch_message(payload.message_id)
            emoji = payload.emoji.name

            result = await database.fetchrow(
                "SELECT * FROM public.roles WHERE message_id=$1 AND emoji=$2",
                payload.message_id,
                emoji,
            )

            if result:
                ini_roles: t.List[discord.Role] = []
                total = 0
                removed = 0
                for role_id in result["roleids"]:
                    total += 1
                    role = ctx.guild.get_role(role_id)
                    if role:
                        ini_roles.append(role)
                    else:
                        removed += 1
                removal = " Those roles are :"
                if removed:
                    removal = (
                        f" {removed} of them didn't exist anymore, so I "
                        "deleted them from my database. "
                        "The remaining roles are :")
                joiner = "\n - "
                await ctx.send(
                    f"{total} roles are already linked to this message and "
                    f"emoji.{removal}\n - "
                    f"{joiner.join([r.name for r in ini_roles])}\n\nDo you "
                    "want me to replace them with the new ones, or add the new"
                    " ones to the list. Send `replace` or `add` in the next 30"
                    " seconds to indicate your choice please.")

                def check3(message: discord.Message) -> bool:
                    """Check the answer."""
                    return message.author == ctx.author and (
                        message.channel == ctx.channel and
                        (message.content.lower().startswith("add") or
                         (message.content.lower().startswith("replace"))))

                try:
                    answer = await self.bot.wait_for(
                        "message",
                        check=check3,
                        timeout=30,
                    )
                except asyncio.TimeoutError:
                    await ctx.send("Cancelling the command...")
                    return
                if answer.content.lower().startswith("add"):
                    roles += ini_roles
                await database.execute(
                    "UPDATE public.roles SET roleids=$1 WHERE message_id=$2 "
                    "AND emoji=$3",
                    [r.id for r in roles],
                    payload.message_id,
                    emoji,
                )
            else:
                await database.execute(
                    "INSERT INTO public.roles VALUES ($1, $2, $3, $4, $5)",
                    payload.message_id,
                    payload.channel_id,
                    payload.guild_id,
                    emoji,
                    [r.id for r in roles],
                )
            try:
                await message.add_reaction(emoji)
            except discord.DiscordException:
                pass
            counter = -1
            reaction = find(
                lambda reaction: getattr(reaction.emoji, "name", reaction.emoji
                                         ) == emoji,
                message.reactions,
            )
            if not reaction:
                await ctx.send("The rule has been successfully updated")
                return
            async for user in reaction.users():
                counter += 1
                try:
                    if isinstance(user, discord.Member):
                        await user.add_roles(*roles)
                except discord.DiscordException:
                    pass
            if counter:
                await ctx.send("The rule has been successfully updated"
                               f" and applied to {str(counter)} users")
            else:
                await ctx.send("The rule has been successfully updated")

    @role.command(aliases=["list", "status"])
    async def info(self, ctx: commands.Context) -> None:
        """Get a list of all the role rules defined for this guild."""
        async with self.bot.pool.acquire() as database:
            result = await database.fetch(
                "SELECT * FROM public.roles WHERE guild_id=$1",
                ctx.guild.id,
            )
            deleted = 0
            output = []
            if result:
                for key in result:
                    try:
                        channel = self.bot.get_channel(key["channel_id"])
                        await channel.fetch_message(key["message_id"])
                        output.append(dict(key))
                        output[-1]["roleids"] = [
                            ID for ID in output[-1]["roleids"]
                            if ctx.guild.get_role(ID)
                        ]
                        await database.execute(
                            "UPDATE public.roles SET roleids=$1 WHERE message_id=$2",
                            output[-1]["roleids"],
                            key["message_id"],
                        )
                    except Exception:
                        deleted += 1
                        await database.execute(
                            "DELETE FROM public.roles WHERE message_id=$1",
                            key["message_id"],
                        )
            if not output:
                embed = discord.Embed(
                    title=f"Rules for guild {ctx.guild.name}",
                    colour=discord.Colour.blue(),
                    description=(
                        "No rules are currently defined for this guild. "
                        f"Create the first one with `{ctx.prefix}role add`"),
                )
                await ctx.send(embed=embed)
                return

            def r_m(role_id: int) -> str:  # role mention
                return ctx.guild.get_role(role_id).mention

            content = [(f"- Rule {i + 1} : "
                        "[Message](https://discord.com/channels/"
                        f"{val['guild_id']}/{val['channel_id']}/"
                        f"{val['message_id']} \"Original message\") | "
                        f"{val['emoji']} | " +
                        ", ".join([r_m(ID) for ID in val["roleids"]]))
                       for i, val in enumerate(output)]

            del_msg = ((f" {deleted} rules were deleted because the "
                        "original message didn't exist anymore")
                       if deleted else "")

            final = [content[0]]
            cur_len = len(content[0])
            for elem in content[1:]:
                if len(elem) + cur_len > 1996 - len(del_msg):
                    final.append(elem)
                    cur_len = len(elem)
                else:
                    cur_len += len(elem) + 1
                    final[-1] += f"\n{elem}"
                # No more than 2048 characters per embed

            if len(final) == 1:
                embed = discord.Embed(
                    title=f"Rules for guild {ctx.guild.name}",
                    colour=discord.Colour.blue(),
                    description=(
                        "You need the rule number for the `remove` action."
                        f"{del_msg}\n\n{final[0]}"),
                )
                await ctx.send(embed=embed)
            else:
                pages = menus.MenuPages(
                    source=RoleSource(final, ctx.guild.name, del_msg),
                    clear_reactions_after=True,
                )
                await pages.start(ctx)

    @role.command(aliases=["delete"])
    async def remove(self, ctx: commands.Context, number: int) -> None:
        """Remove the rule associated with the number specified."""
        async with self.bot.pool.acquire() as database:
            try:
                result = await database.fetch(
                    "SELECT * FROM public.roles WHERE guild_id=$1",
                    ctx.guild.id,
                )[number - 1]
            except IndexError:
                await ctx.send(
                    "The rule you are trying to delete doesn't exist")
                return
            try:
                await self.bot.get_channel(result["channel_id"]
                                           ).fetch_message(result["message_id"]
                                                           )
                roles: t.List[discord.Role] = []
                for role_id in result["roleids"]:
                    role = ctx.guild.get_role(role_id)
                    if role:
                        roles.append((role_id, role.name))
                await database.execute(
                    "UPDATE public.roles SET roleids=$1 WHERE message_id=$2",
                    [r[0] for r in roles],
                    result["message_id"],
                )
                embed = discord.Embed(
                    title=f"Informations about rule number {number}", )
                embed.add_field(
                    name="Message :",
                    value=("[Click here](https://discord.com/channels/"
                           f'{result["guild_id"]}/{result["channel_id"]}/'
                           f'{result["message_id"]} '
                           '"Link to the original message")'),
                )
                embed.add_field(name="Emoji :", value=result["emoji"])
                embed.add_field(
                    name="Roles :",
                    value=" - " + "\n - ".join([
                        f"Role n°{i + 1}: {roles[i][1]}"
                        for i in range(len(roles))
                    ]),
                )
                await ctx.send(embed=embed)
                await ctx.send(
                    "Please enter a comma-separated list of the numbers of the"
                    " roles you want to remove in less than 30 seconds")

                def check(message: discord.Message) -> bool:
                    """Check for digits."""
                    return message.author == ctx.author and (
                        message.channel == ctx.channel
                        and all(k.isdigit() for k in message.content.replace(
                            " ", "").split(",")))

                try:
                    message = await self.bot.wait_for(
                        "message",
                        check=check,
                        timeout=30,
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        "You didn't answer in time. I'm ignoring this command")
                    return

                role_numbers = [
                    int(k) for k in message.content.replace(" ", "").split(",")
                ]

                if not all(0 < k <= len(roles) for k in role_numbers):
                    await ctx.send(
                        "You entered wrong values for the indexes. "
                        "Please re-run the command with correct values.")
                else:
                    await database.execute(
                        "UPDATE public.roles set roleids=$1 WHERE message_id=$2",
                        [
                            roles[i][0] for i in range(len(roles))
                            if not i + 1 in role_numbers
                        ],
                        result["message_id"],
                    )
                    await ctx.send(
                        f"I successfully removed those {len(role_numbers)} "
                        "roles from the rule")
            except discord.NotFound:
                await database.execute(
                    "DELETE FROM public.roles WHERE message_id=$1",
                    result["message_id"],
                )
                await ctx.send(
                    "The message associated with this rule has been deleted. "
                    "I thus removed the rule.")
                return

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(administrator=True)
    async def swear(self,
                    ctx: commands.Context,
                    word: t.Optional[str] = None) -> None:
        """Manage the swear filter.

        `on`/`off` : turns the filter on/off.
        `auto` : turns autodetection on/off.
        `notification` : turns DM alert on/off (guild owner only).
        Anything else adds a word to the list
        Nothing means to check the status
        NO SWEAR WORDS IN MY CHRISTIAN SERVER !
        """
        owner = ctx.guild.owner or await ctx.guild.fetch_member(
            ctx.guild.owner_id)
        async with self.bot.pool.acquire() as database:
            if word:
                word = word.lower()
                if word == "on":
                    await database.execute(
                        "INSERT INTO public.swear (id, manual_on) VALUES "
                        "($1, True) ON CONFLICT (id) DO UPDATE SET "
                        "manual_on=True",
                        ctx.guild.id,
                    )
                    await ctx.send("Swear filter turned on")
                elif word == "off":
                    await database.execute(
                        "INSERT INTO public.swear (id, manual_on) VALUES "
                        "($1, False) ON CONFLICT (id) DO UPDATE SET "
                        "manual_on=False",
                        ctx.guild.id,
                    )
                    await ctx.send("Swear filter turned off")
                elif word == "auto":
                    result = await database.fetchrow(
                        "SELECT * FROM public.swear WHERE id=$1",
                        ctx.guild.id,
                    )
                    if result:
                        if result.get("auto"):
                            await database.execute(
                                "UPDATE public.swear SET autoswear=False WHERE"
                                " id=$1",
                                ctx.guild.id,
                            )
                            await ctx.send("Autodetection turned off")
                        else:
                            await database.execute(
                                "UPDATE public.swear SET autoswear=True WHERE id=$1",
                                ctx.guild.id,
                            )
                            await ctx.send("Autodetection turned on")
                    else:
                        await database.execute(
                            "INSERT INTO public.swear (id, autoswear) VALUES "
                            "($1, True)",
                            ctx.guild.id,
                        )
                        await ctx.send("Autodetection turned on")
                elif word == "notification":
                    if ctx.author != owner:
                        await ctx.send(
                            "As he is the one alerted, only the guild owner "
                            "can change this setting")
                        return
                    result = await database.fetchrow(
                        "SELECT * FROM public.swear WHERE id=$1",
                        ctx.guild.id,
                    )
                    if result:
                        if result.get("notification"):
                            await database.execute(
                                "UPDATE public.swear SET notification=False "
                                "WHERE id=$1",
                                ctx.guild.id,
                            )
                            await ctx.send("The alert has been disabled")
                        else:
                            await database.execute(
                                "UPDATE public.swear SET notification=True "
                                "WHERE id=$1",
                                ctx.guild.id,
                            )
                            await ctx.send("The alert has been enabled")
                    else:
                        await database.execute(
                            "INSERT INTO public.swear (id, notification) "
                            "VALUES ($1, False)",
                            ctx.guild.id,
                        )
                        await ctx.send("The alert has been disabled")
                else:
                    result = await database.fetchrow(
                        "SELECT * FROM public.swear WHERE id=$1",
                        ctx.guild.id,
                    )
                    if result:
                        word_list = result["words"]
                        if word in word_list:
                            word_list.remove(word)
                            await ctx.send(
                                f"The word `{word}` was removed from this "
                                "guild's list of swear words")
                        else:
                            word_list.append(word)
                            await ctx.send(
                                f"The word `{word}` was added to this guild's"
                                " list of swear words")
                    else:
                        word_list = [word]
                        await ctx.send(
                            f"The word `{word}` was added to this guild's "
                            "list of swear words")
                    await database.execute(
                        "INSERT INTO public.swear (id, words) VALUES ($1, $2)"
                        " ON CONFLICT (id) DO UPDATE set words=$2",
                        ctx.guild.id,
                        word_list,
                    )
            else:
                status = await database.fetchrow(
                    "SELECT * FROM public.swear WHERE id=$1",
                    ctx.guild.id,
                )
                if not status:
                    status = {
                        "manual_on": True,
                        "autoswear": False,
                        "notification": True,
                        "words": [],
                    }

                embed = discord.Embed(
                    title=f"Swear words in {ctx.guild.name}",
                    colour=0xFFFF00,
                )
                embed.add_field(
                    name="Manual filter status",
                    value="Online" if status["manual_on"] else "Offline",
                )
                embed.add_field(
                    name="Auto filter status",
                    value="Online" if status["autoswear"] else "Offline",
                )
                embed.add_field(
                    name=("Alert message status (in case I cannot delete a message)"
                          ),
                    value="Enabled" if status["notification"] else "Disabled",
                )
                embed.add_field(
                    name="Guild-specific swear words",
                    value=(" - " +
                           "\n - ".join(status["words"]) if status["words"]
                           else "No swear words are defined for this guild"),
                    inline=False,
                )
                await ctx.send(embed=embed)

    @commands.Cog.listener("on_raw_reaction_add")
    async def role_adder(
        self,
        payload: discord.RawReactionActionEvent,
    ) -> None:
        """Add a role on reaction."""
        if not self._role_add:
            self._role_add = await self.bot.pool.acquire()
            self._role_add_lock = asyncio.Lock()
        async with self._role_add_lock:
            result = await self._role_add.fetchrow(
                "SELECT * FROM public.roles WHERE message_id=$1 AND emoji=$2",
                payload.message_id,
                payload.emoji.name,
            )
            if result:
                guild = self.bot.get_guild(payload.guild_id)
                roles = (guild.get_role(r) for r in result["roleids"])
                try:
                    await payload.member.add_roles(
                        *(r for r in roles if r),
                        reason=f"Rule for emoji {payload.emoji.name}",
                    )
                except discord.DiscordException:
                    pass

    @commands.Cog.listener("on_raw_reaction_remove")
    async def role_remover(
        self,
        payload: discord.RawReactionActionEvent,
    ) -> None:
        """Remove the role."""
        if not self._role_remove:
            self._role_remove = await self.bot.pool.acquire()
            self._role_remove_lock = asyncio.Lock()
        async with self._role_remove_lock:
            result = await self._role_remove.fetchrow(
                "SELECT * FROM public.roles WHERE message_id=$1 AND emoji=$2",
                payload.message_id,
                payload.emoji.name,
            )
            if result:
                guild = self.bot.get_guild(payload.guild_id)
                try:
                    member = guild.get_member(
                        payload.user_id) or await guild.fetch_member(
                            payload.user_id)
                except discord.HTTPException:
                    return
                roles = (guild.get_role(r) for r in result["roleids"])
                try:
                    await member.remove_roles(
                        *(r for r in roles if r),
                        reason=f"Rule for emoji {payload.emoji.name}",
                    )
                except discord.DiscordException:
                    pass

    @commands.Cog.listener("on_member_join")
    async def role_saver(self, member: discord.Member) -> None:
        """Give roles on join."""
        if not self._role_save:
            self._role_save = await self.bot.pool.acquire()
            self._role_save_lock = asyncio.Lock()
        async with self._role_save_lock:
            results = await self._role_save.fetch(
                "SELECT * FROM public.roles WHERE guild_id=$1",
                member.guild.id,
            )
            for result in results:
                channel = member.guild.get_channel(result["channel_id"])
                if channel:
                    message = await channel.fetch_message(result["message_id"])
                    if message:
                        for reaction in message.reactions:
                            emoji = reaction.emoji
                            if not isinstance(emoji, str):
                                emoji = emoji.name
                            if emoji == result["emoji"]:
                                async for user in reaction.users():
                                    if user == member:
                                        roles = (member.guild.get_role(r)
                                                 for r in result["roleids"])
                                        await member.add_roles(
                                            *(r for r in roles if r),
                                            reason=f"Rule for emoji {emoji}",
                                        )
                                        break

    @commands.Cog.listener("on_message")
    async def no_swear_words(self, message: discord.Message) -> None:
        """Delete swear words."""
        if (message.author == self.bot
                or isinstance(message.author, discord.User)
                or not isinstance(message.channel, discord.TextChannel)):
            return
        if message.channel.is_nsfw() or (
                message.author.guild_permissions.manage_messages):
            return
        if not self._swear_conn:
            self._swear_conn = await self.bot.pool.acquire()
            self._swear_conn_lock = asyncio.Lock()
        async with self._swear_conn_lock:
            try:
                status = await self._swear_conn.fetchrow(
                    "SELECT * FROM public.swear WHERE id=$1",
                    message.guild.id,
                )
                if not status:
                    return
                owner = message.guild.owner or await message.guild.fetch_member(
                    message.guild.owner_id)
                if status["autoswear"]:
                    for word in auto_swear_detection:
                        if word in message.content.lower().split(" "):
                            try:
                                await message.delete()
                                await message.channel.send(
                                    f"Sorry {message.author.mention}. I "
                                    "deleted your message because it contained"
                                    " a forbidden word",
                                    delete_after=5,
                                )
                            except discord.Forbidden:
                                if status["notification"]:
                                    await owner.send(
                                        f"{message.author} used a swear word :"
                                        f" `{word}`, but I lack the permission"
                                        "s to delete the message. Please give "
                                        "them back to me. You can use "
                                        "the command `swear notification` to "
                                        "turn this alert off.")
                            return
                if status["manual_on"]:
                    for word in status["words"]:
                        if word in message.content.lower().split(" "):
                            try:
                                await message.delete()
                                await message.channel.send(
                                    f"Sorry {message.author.mention}. I "
                                    "deleted your message because it contained"
                                    " a forbidden word",
                                    delete_after=5,
                                )
                            except discord.Forbidden:
                                if status["notification"]:
                                    await owner.send(
                                        f"{message.author} used a swear word :"
                                        f" `{word}`, but I lack the permission"
                                        "s to delete the message. Please give "
                                        "them back to me. You can use the "
                                        "command `swear notification` "
                                        "to turn this alert off.")
                            break
            except discord.DiscordException:
                pass

    def cog_unload(self) -> None:
        """Cleanup the connections."""
        for name in ("_swear_conn", "_role_save", "_role_add", "_role_remove"):
            conn = getattr(self, name, None)
            if conn:
                asyncio.create_task(self.bot.pool.release(conn))


def setup(bot: commands.Bot) -> None:
    """Load the Moderation cog."""
    bot.add_cog(Moderation(bot))
