import asyncio
import jcore.client
from jcore.message import CommandMessage
from jcore.helpers import Settings
import logging

class Jarvis(jcore.client.Client):

    async def on_command(self, message: CommandMessage):
        if message.KEYWORD == "sleep":
            await message.send("returning your message after 10 seconds")
            await asyncio.sleep(10)
            await message.send(f"""return: `{message.message_text.replace("!sleep", "").strip()}`""")
        if message.KEYWORD == "followers":
            await message.send("enabled follower only mode.")
            await message.followers()





if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('jcore')
    logger.setLevel(logging.DEBUG)
    format = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    fileHandler = logging.FileHandler(filename='jarvis.log', encoding='utf-8', mode='w')
    fileHandler.setFormatter(format)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(format)
    streamHandler.setLevel(logging.INFO)
    logger.addHandler(streamHandler)


    config = Settings().get_all_settings()
    client = Jarvis("Test Client", config["channels"])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.run())
    loop.close()