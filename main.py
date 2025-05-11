import os
import discord

from discord.ext import commands
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN not found in .env file")


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(
), application_id=1371157657838288906)  # Replace with your bot's application ID


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print("------")
    await bot.change_presence(activity=discord.Game(name="with coffee!"))
    print("Bot is ready!")


def main():
    bot.load_extension("cogs.coffee")
    bot.run(TOKEN)


main()
