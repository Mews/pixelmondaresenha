from dotenv import load_dotenv
import os
import discord
import logging
from aternos import *
import asyncio
from functools import reduce

load_dotenv()
BOT_TOKEN = str(os.environ["BOT_TOKEN"])
LOG_REFRESH_RATE = 10 # seconds

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8", mode="w"),
    ]
)

#handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
mention_everyone = discord.AllowedMentions(everyone=True)


def get_message_channel():
    return client.get_channel(1335723656067940422)


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
        from pprint import pprint
        new_log_content = log_content.replace(prev_log_content, "")

        if new_log_content:
            list(map(logging.info, ["\nNew log messages:"]+new_log_content.split("\n")[:-1]))

        if all(msg in new_log_content for msg in ["[Pixelmon]", "has spawned in a", "biome!"]):
            # ping @everyone
            line = reduce(lambda p, line: line if all(msg in line for msg in ["[Pixelmon]", "has spawned in a", "biome!"]) else "",
                          new_log_content.split("\n"), 
                          "")
            c.send(f"{line}\n@everyone", allowed_mentions=mention_everyone)

        prev_log_content = log_content

        await asyncio.sleep(LOG_REFRESH_RATE)


if __name__ == "__main__":
    #client.run(BOT_TOKEN)
    client.run(BOT_TOKEN, root_logger=True)
