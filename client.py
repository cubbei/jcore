import asyncio
import jsocket

from config import load_settings
from log import log
from time import sleep, time






class Client():

    def __init__(self, name:str, channels: list):
        self.name = name
        self.channels = channels
        self.socket = jsocket.Socket(self)
        
        
    
    async def run(self):
        await self.socket.connect()
        await asyncio.sleep(0.001)
        await self.socket.run()

    async def on_socket_recieve(self, socket_message: str):
        pm = "PRIVMSG"
        if pm in socket_message:
            msg = self.__get_message(socket_message, pm)
            channel = self.__get_channel(socket_message, pm)

            if "!sleep" in socket_message:
                await self.socket.send(channel, "returning your message after 10 seconds")
                await asyncio.sleep(10)
                await self.socket.send(channel, f"""return: `{msg.replace("!sleep ", "")}`""")

    
    def __get_channel(self, line: str, key: str) -> str:
        try:
            l = line.split(f"{key} #", 1)[1]
            try:
                return l.split(" ", 1)[0]
            except IndexError:
                return l
        except IndexError:
            return None

    def __get_message(self, line: str, key: str) -> str:
        try:
            return line.split(f" {key} #",1)[1].split(" ",1)[1][1:].strip()
        except IndexError:
            return None





config = load_settings()
client = Client("Test Client", config["channels"])
loop = asyncio.get_event_loop()

loop.run_until_complete(client.run())
loop.close()