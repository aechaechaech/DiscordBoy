import discord, logging, secrets, multiprocessing, PIL, time
from pyboy import PyBoy, WindowEvent, botsupport
from os import getcwd
from io import BytesIO

logging.basicConfig(level=logging.INFO)

client = discord.Client()

test_rom = getcwd() + "\\bot\\roms\\mario.gb"

frame_queue = multiprocessing.Queue()


def pyboy_thread(frame_queue):
    pyboy = PyBoy(test_rom, window_type="SDL2", window_scale=3, debug=False, game_wrapper=True)
    bot_support_manager = pyboy.botsupport_manager()
    bot_support_screen = bot_support_manager.screen()

    mario = pyboy.game_wrapper()
    mario.start_game()

    while True:
        pyboy.tick()   

        if frame_queue.empty():
            frame_data = bot_support_screen.screen_ndarray()
            frame_queue.put(frame_data)

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

        if msg[0] == "frame":
            image_data = frame_queue.get()
            frame = PIL.Image.fromarray(image_data, "RGB")
            with BytesIO() as image_binary:
                frame.save(image_binary, 'PNG')
                image_binary.seek(0)
                await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))


        # help menu
        # \u200b is a zero width white space charecter
        # there cuz i think it looks better with no name
        if msg[0] == "help":
            embedVar = discord.Embed(title="Help Menu", color=0x00ff00)
            embedVar.add_field(name ="\u200b", value="`start rom`: play game", inline=False)
            await message.channel.send(embed=embedVar)

if __name__ == "__main__":
    boy_thread = multiprocessing.Process(target=pyboy_thread, args=(frame_queue,))
    boy_thread.start()

    client.run(secrets.bot_token)