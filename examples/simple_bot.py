import asyncio
import jcore
from jcore.message import CommandMessage


class SimpleBot(jcore.Client):

    async def on_command(self, message: CommandMessage):
        if message.KEYWORD == "hi":
            await message.send(f"hello {message.display_name}")


if __name__ == "__main__":
    client = SimpleBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.run())
    loop.close()