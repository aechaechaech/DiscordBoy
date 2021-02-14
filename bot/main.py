from tinydb import Query, database, TinyDB
import discord, logging, secrets, re

logging.basicConfig(level=logging.INFO)

client = discord.Client()

test_line = "#" * 160
test_screen = (test_line + "\n") * 144

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await client.change_presence(activity=discord.Game(name="!!!help for help menu"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?gb'):
        msg = message.content[3:]
        msg = msg.split()

        if msg[0] == "start":
            embedVar = discord.Embed(title="Test Screen", color=0x00ff00)
            embedVar.add_field(name ="\u200b", value=f"`{test_screen}`", inline=False)
            await message.channel.send(embed=embedVar)

        # help menu
        # \u200b is a zero width white space charecter
        # there cuz i think it looks better with no name
        if msg[0] == "help":
            embedVar = discord.Embed(title="Help Menu", color=0x00ff00)
            embedVar.add_field(name ="\u200b", value="`start rom`: play game", inline=False)
            await message.channel.send(embed=embedVar)


client.run(secrets.bot_token)