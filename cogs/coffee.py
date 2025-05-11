import discord
import asyncio
from discord.ext import commands
import random

# frases carismaticas
phrases = {
    'not available': [
        'Esse comando não está disponível nesse servidor.',
    ],
    'not in voice': [
        'Você não está em um canal de voz.',
        'Você precisa estar em um canal de voz para usar esse comando.',
    ],
    'already in coffee': [
        'Você já está na pausa de café.',
        'Você já está em um canal de café.',
    ],
    'coffee started': [
        'Pausa para o café iniciada!',
        'Pausa para o café começando agora!',
    ],

    'minutes': [
        '{} minutos de pausa para o café!',
        'Você tem {} minutos para tomar seu café!',
        'Aproveite seus {} minutos de café!',
        'Você tem {} minutos para relaxar e tomar seu café!',
        'Aproveite seus {} minutos de pausa para o café!',
        'Você tem {} minutos para tomar seu café e relaxar!',
    ],
    'coffee ended': [
        'Pausa para o café encerrada!',
        'Pausa para o café acabou!',
        'Pausa para o café finalizada!',
        'Pausa para o café terminada!',
        'Pausa para o café concluída!',
        'Pausa para o café encerrada com sucesso!',
    ],
}


class CoffeeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="coffee", description="Pause for coffee")
    @discord.option(
        "minutes",
        description="Minutes to pause for coffee",
        default=5,
        min_value=2,
        max_value=20,
    )
    async def coffee(self, ctx: discord.ApplicationContext, minutes: int):
        ids = {
            1371180999555289098: 1371200551731331112,
            1333894961669738516: 1369442331236765756,
        }

        guild = ctx.guild

        if guild.id not in ids:
            await ctx.respond(random.choice(phrases['not available']))
            return

        if ctx.author.voice is None:
            await ctx.respond(random.choice(phrases['not in voice']))
            return

        if ctx.author.voice.channel.id == ids[guild.id]:
            await ctx.respond(random.choice(phrases['already in coffee']))
            return

        users = ctx.author.voice.channel.members

        await ctx.respond(random.choice(phrases['coffee started']))

        coffee_channel = guild.get_channel(ids[guild.id])
        original_channel = ctx.author.voice.channel

        await self.move_to_coffee(users, coffee_channel)

        await ctx.channel.send(random.choice(phrases['minutes']
                                             ).format(minutes))

        await asyncio.sleep(minutes * 60)

        await self.move_to_original(users, original_channel)

        await ctx.respond(random.choice(phrases['coffee ended']))

    async def move_to_coffee(self, users: list[discord.Member],
                             coffee_channel: discord.VoiceChannel):
        for user in users:
            await user.move_to(coffee_channel)

    async def move_to_original(self, users: list[discord.Member],
                               original_channel: discord.VoiceChannel):
        for user in users:
            try:
                await user.move_to(original_channel)
            except discord.HTTPException:
                # Ignore if the user is not in a voice channel
                pass


def setup(bot: commands.Bot):
    bot.add_cog(CoffeeCog(bot))
