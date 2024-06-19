import discord
import os
from dotenv import load_dotenv
import bot  # Assuming `bot.py` contains the `get_response` function

load_dotenv()
discord_key = os.getenv('TOKEN') 
print(discord_key)


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Your bot's ID and your own ID
my_bot_id = int(os.getenv('BOT_ID'))
my_id = int(os.getenv('MY_ID'))

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author.id != my_bot_id:
        if isinstance(message.channel, discord.TextChannel) and message.channel.name == 'get-code':
            response = message.content
            print(response)
            final_ans = bot.get_response(response) 
            await message.channel.send(final_ans)

client.run(discord_key)
