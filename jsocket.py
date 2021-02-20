import asyncio
import socket
import traceback


from datetime import datetime
from config import load_settings
from log import debug, info, critical, warning

INTERVAL = 0.001


class Socket():

    def __init__(self, client, verbose: bool = True):
        self.active = True
        self.client = client
        self.channels = client.channels
        self.buffer = ""
        self.verbose = verbose
        self.socket = None
        config = load_settings()
        self.nick = config["nick"]
        self.token = config["token"]
        self.loop = asyncio.get_event_loop()

    


    async def connect(self):
        info(f"Initialising connection to: {self.channels}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("irc.chat.twitch.tv", 6667))
        await self._send_raw(f"PASS {self.token}")
        await self._send_raw(f"NICK {self.nick}")
        await self._send_raw("CAP REQ :twitch.tv/membership")
        await self._send_raw("CAP REQ :twitch.tv/tags")
        await self._send_raw("CAP REQ :twitch.tv/commands")
        for channel in self.channels:
            await self._send_raw(f"JOIN #{channel} ")
        self.last_ping = datetime.now()
        info("Socket engaged.")


    async def disconnect(self):
        if self.verbose:
            info("departing channels")
        try:
            for channel in self.channels:
                await self._send_raw(f"PART #{channel} ")
        except Exception as e:
            critical(f"Suppressing a caught an exception in `Socket.disconnect()` [Parting channel]. Details below\n{type(e)}: {traceback.format_exc()}")
        try:
            self.socket.close()
        except Exception as e:
            critical(f"Suppressing a caught an exception in `Socket.disconnect()` [closing socket]. Details below\n{type(e)}: {traceback.format_exc()}")

    async def reconnect(self):
        if self.verbose:
            info("Reconnect detected!")
        self.disconnect()
        if self.verbose:
            info("Waiting to reconnect.")
        await asyncio.sleep(10)
        await self.connect()



    async def send(self, channel: str, message: str):
        await self._send_raw(f"PRIVMSG #{channel.lower()} :{message}")

    async def _send_raw(self, message: str):
        try:
            if self.verbose:
                if message[:4] == "PASS":
                    debug(f" < PASS ****")
                else:
                    debug(f" < {message}")
            self.socket.send((f"{message}\r\n").encode('utf-8'))
            await asyncio.sleep(INTERVAL)
        except OSError:
            critical(f"Socket is closed and must be reopened to send the message '{message}'")


    async def run(self):
        try:
            while self.active:
                
                await self.__process_stream_data()
            try:
                self.socket.close()
            except Exception as e:
                critical(f"Suppressing a caught an exception while attempting to close the socket in `Socket.run()`. Details below\n{type(e)}: {traceback.format_exc()}")
        finally: 
            if (self.socket):
                self.disconnect()




    async def __process_stream_data(self):
        try:
            self.buffer = self.buffer + (await self.loop.sock_recv(self.socket, 1024)).decode()
        except ConnectionAbortedError:
            info("Socket connection has Closed")
        except UnicodeDecodeError:
            warning(f"Unicode Decode error detected, possible issue with the buffer.\nBuffer: [{self.buffer}]\n\nRegenerating buffer...")
            self.buffer = ""
            info("Buffer regeneration completed.")
        except OSError:
            warning("OSError detected, socket issue identitfied. Attempting to recover socket.")
            await self.reconnect()

        temp = self.buffer.split("\n")
        self.buffer = temp.pop()
        for line in temp:
            debug(f" > {line}")
            if ("PING :tmi.twitch.tv" in line): # Keep Alive Mechanism
                await self._send_raw("PONG :tmi.twitch.tv")
                self.last_ping = datetime.now()
            await asyncio.sleep(INTERVAL)
            self.loop.create_task(self.client.on_socket_recieve(line))
        