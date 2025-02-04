from dotenv import load_dotenv
import os
import discord
import logging
from aternos import *
import asyncio
from functools import reduce
import re
from datetime import datetime
import os

load_dotenv()
BOT_TOKEN = str(os.environ["BOT_TOKEN"])
LOG_REFRESH_RATE = 10 # seconds

if not os.path.exists("logs"):
    logging.info("No logs folder was found, creating it")
    os.makedirs("logs")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(f"logs/{datetime.now().strftime("%H-%M %d-%m-%Y")}.log", encoding="utf-8", mode="w"),
    ]
)

#handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
mention_everyone = discord.AllowedMentions(everyone=True)


def get_message_channel():
    try:
        channel_id = int(os.environ["DISCORD_CHANNEL_ID"])
        
        channel = client.get_channel(channel_id)

        logging.info(f"Loaded output channel {channel.name} with id {channel.id}")

        return channel
    
    except ValueError:
        logging.ERROR("Found invalid discord channel id")

        raise ValueError("Invalid DISCORD_CHANNEL_ID")



@client.event
async def on_ready():
    global driver

    logging.info(f"BOT STARTED AS {client.user.name}")

    driver = create_driver()
    open_server_log(driver)
    await asyncio.sleep(1)
    await loop()


async def loop():
    await client.wait_until_ready()
    c = get_message_channel()

    prev_log_content = get_log_content(driver)
    while not client.is_closed():
        log_content = get_log_content(driver)
        new_log_content = log_content.replace(prev_log_content, "")

        if new_log_content:
            list(map(lambda log_line:logging.info(f"Log message: {log_line}"), new_log_content.split("\n")[:-1]))

        if all(msg in new_log_content for msg in ["[Pixelmon]", "has spawned in a", "biome!"]):
            # ping @everyone
            spawn_regex = re.compile( r"\[Pixelmon\] ((.+) has spawned in a (.+) biome)" )
            coords_regex = re.compile( r"Spawned (.+) at: (.*)" )

            spawn_message = spawn_regex.search(new_log_content).group(1)
            coords_message = coords_regex.search(new_log_content).group(0)

            # mention @everyone
            await c.send(f"@everyone", allowed_mentions=mention_everyone)
            # send legendary spawn message and coords
            await c.send(f"{spawn_message}\n{coords_message}")

        prev_log_content = log_content

        await asyncio.sleep(LOG_REFRESH_RATE)


if __name__ == "__main__":
    #client.run(BOT_TOKEN)
    client.run(BOT_TOKEN, root_logger=True)
