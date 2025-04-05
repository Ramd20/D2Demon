import discord

from D2.responses import handleResponses
from D2.scraper import getMenu
from SecretToken import SECRET_TOKEN

def run_discord_bot():
    TOKEN = SECRET_TOKEN

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.content[0] == "!":
            message.content = message.content[1:]
            if handleResponses(message.content) == 4:
                await message.channel.send("This command is not available")
            else:
                string = getMenu(handleResponses(message.content))

                done = False
                start = 0

                while not done:
                    indexOne = string.index("[", start)
                    if "[" not in string[indexOne + 1:]:
                        await message.channel.send(string[indexOne:].strip())
                        done = True
                    else:
                        indexTwo = string.index("[", indexOne + 1)
                        await message.channel.send(string[indexOne:indexTwo].strip())
                        start = indexTwo



    client.run(TOKEN)

