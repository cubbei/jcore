import asyncio
from jcore.exceptions import JarvisException
import socket
import traceback
import uuid
import logging


from datetime import datetime
from jcore.helpers import Settings
from .messageparser import parse_line


INTERVAL = 0.001

log = logging.getLogger(f"{__name__} [{uuid.uuid4().hex[:8]}]")

class Socket():
    """A wrapper for the low-level core library socket interface, 
    and customised to facilitate communication with the Twitch IRC API."""

    def __init__(self, client, command_activator: str):
        self.client = client
        self.command_activator = command_activator
        self.active = True
        self.__channels = []
        self.buffer = ""
        self.socket = None
        config = Settings().get_all_settings()
        self.nick = config["nick"]
        self.token = config["token"]
        self.loop = asyncio.get_event_loop()

    def set_channels(self, channels: list):
        self.__channels = channels

    @property
    def current_connections(self) -> int:
        return len(self.__channels)


    async def connect(self):
        if len(self.__channels) == 0: 
            raise Exception("Channels list hasn't been set.")
        log.info(f"Initialising connection to: {self.__channels}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("irc.chat.twitch.tv", 6667))
        await self._send_raw(f"PASS {self.token}")
        await self._send_raw(f"NICK {self.nick}")
        await self._send_raw("CAP REQ :twitch.tv/membership")
        await self._send_raw("CAP REQ :twitch.tv/tags")
        await self._send_raw("CAP REQ :twitch.tv/commands")
        for channel in self.__channels:
            await self._join(channel)
        self.last_ping = datetime.now()
        log.info(f"Socket engaged.")


    async def disconnect(self):
        try:
            log.info(f"departing channels")
            try:
                tasks = []
                for channel in self.__channels:
                    tasks.append(await self._part(channel))
                asyncio.gather(tasks, loop=self.loop)
            except Exception as e:
                log.critical(f"Suppressing a caught an exception in `Socket.disconnect()` [Parting channel]. Details below\n{type(e)}: {traceback.format_exc()}")
            try:
                self.socket.close()
            except Exception as e:
                log.critical(f"Suppressing a caught an exception in `Socket.disconnect()` [closing socket]. Details below\n{type(e)}: {traceback.format_exc()}")
        except Exception:
            log.critical(f"Failed to correctly disconnect from channel")

    async def reconnect(self):
        log.info(f"Reconnect detected!")
        await self.disconnect()
        log.info(f"Waiting to reconnect.")
        await asyncio.sleep(10)
        await self.connect()


    async def _join(self, channel):
        await self._send_raw(f"JOIN #{channel} ")

    async def _part(self, channel):
        await self._send_raw(f"PART #{channel} ")

    async def join_channel(self, channel):
        log.info(f"Sending request to join channel `{channel}`")
        try:
            self.__channels.append(channel)
            await self._join(channel)
        except JarvisException as ex:
            log.error(f"An error occurred when attemting to leave the channel `{channel}`\nDetails below\n{type(ex)}: {traceback.format_exc()}")
            return
        if channel in self.__channels:
            log.info(f"Successfully joined channel `{channel}`")
        else:
            log.warning(f"There was an issue adding the channel `{channel}`, check the logs for any further details.")

    
    async def depart_channel(self, channel):
        log.info(f"Sending request to leave channel `{channel}`")
        try:
            self.__channels.remove(channel)
            await self._part(channel)
        except JarvisException as ex:
            log.error(f"An error occurred when attemting to leave the channel `{channel}`\nDetails below\n{type(ex)}: {traceback.format_exc()}")
            return
        if channel not in self.__channels:
            log.info(f"Successfully departed channel `{channel}`")
        else:
            log.warning(f"There was an issue removing the channel `{channel}`, check the logs for any further details.")


    def has_channel(self, channel) -> bool:
        return channel in self.__channels



    async def send(self, channel: str, message: str):
        log.info(f"Sent ({channel}): {message}")
        await self._send_raw(f"PRIVMSG #{channel.lower()} :{message}")

    async def _send_raw(self, message: str):
        try:
            if message[:4] == "PASS":
                log.debug(f" < PASS ****")
            else:
                log.debug(f" < {message}")
            self.socket.send((f"{message}\r\n").encode('utf-8'))
            await asyncio.sleep(INTERVAL)
        except OSError:
            log.critical(f"Socket is closed and must be reopened to send the message '{message}'")


    async def run(self):
        try:
            while self.active:
                await self.__process_stream_message()
            try:
                self.socket.close()
            except Exception as e:
                log.critical(f"Suppressing a caught an exception while attempting to close the socket in `Socket.run()`. Details below\n{type(e)}: {traceback.format_exc()}")
        finally: 
            log.info(f"Closing socket.")
            if (self.socket):
                await self.disconnect()




    async def __process_stream_message(self):
        try:
            self.buffer = self.buffer + (await self.loop.sock_recv(self.socket, 1024)).decode()
        except ConnectionAbortedError:
            log.info(f"Socket connection has Closed")
            await self.reconnect()
        except UnicodeDecodeError:
            log.warning(f"Unicode Decode error detected, possible issue with the buffer.\nBuffer: [{self.buffer}]\n\nRegenerating buffer...")
            self.buffer = ""
            log.info(f"Buffer regeneration completed.")
        except OSError:
            log.warning(f"OSError detected, socket issue identitfied. Attempting to recover socket.")
            await self.reconnect()

        temp = self.buffer.split("\n")
        self.buffer = temp.pop()
        for line in temp:
            log.debug(f" > {line.strip()}")
            if ("PING :tmi.twitch.tv" in line): # Keep Alive Mechanism
                await self._send_raw("PONG :tmi.twitch.tv")
                self.last_ping = datetime.now()
                continue
            await asyncio.sleep(INTERVAL)
            self.loop.create_task(self.__process_line(line))

    async def __process_line(self, line_text):
        message = parse_line(line_text, self.command_activator)
        message.set_socket(self)
        self.loop.create_task(self.client._scb_on_raw(message))

        if message.inner == "Message":
            self.loop.create_task(self.client._scb_on_message(message))
        elif message.inner == "Join":
            self.loop.create_task(self.client._scb_on_join(message))
        elif message.inner == "Mode":
            self.loop.create_task(self.client._scb_on_mode(message))
        elif message.inner == "Names":
            self.loop.create_task(self.client._scb_on_names(message))
        elif message.inner == "Part":
            self.loop.create_task(self.client._scb_on_part(message))
        elif message.inner == "ClearChat":
            self.loop.create_task(self.client._scb_on_clearchat(message))
        elif message.inner == "ClearMessage":
            self.loop.create_task(self.client._scb_on_clearmessage(message))
        elif message.inner == "HostTarget":
            self.loop.create_task(self.client._scb_on_hosttarget(message))
        elif message.inner == "Notice":
            self.loop.create_task(self.client._scb_on_notice(message))
        elif message.inner == "Reconnect":
            self.loop.create_task(self.client._scb_on_reconnect(message))
        elif message.inner == "RoomState":
            self.loop.create_task(self.client._scb_on_roomstate(message))
        elif message.inner == "UserState":
            self.loop.create_task(self.client._scb_on_userstate(message))
        elif message.inner == "GlobalUserState":
            self.loop.create_task(self.client._scb_on_globaluserstate(message))
        elif message.inner == "UserNotice":
            self.loop.create_task(self.client._scb_on_usernotice(message))
        elif message.inner == "RitualUserNotice":
            self.loop.create_task(self.client._scb_on_ritual_usernotice(message))
        elif message.inner == "BitBadgeUpgradeUserNotice":
            self.loop.create_task(self.client._scb_on_bitbadgeupgrade_usernotice(message))
        elif message.inner == "RaidUserNotice":
            self.loop.create_task(self.client._scb_on_raid_usernotice(message))
        elif message.inner == "Whisper":
            log.info(f"[WHISPER]: ({message.display_name}) {message.message_text}")
            self.loop.create_task(self.client._scb_on_whisper(message))
        elif message.inner == "SubscriberUserNotice":
            if message.display_name.lower() != self.nick.lower():
                self.loop.create_task(self.client._scb_on_subscriber_usernotice(message))
        elif message.inner == "GiftedSubscriberUserNotice":
            if message.display_name.lower() != self.nick.lower():
                self.loop.create_task(self.client._scb_on_giftedsubscriber_usernotice(message))
        elif message.inner == "PrivateMessage":
            if message.display_name.lower() != self.nick.lower():
                log.info(f"[CHAT].[{message.channel}]: ({message.display_name}) {message.message_text}")
                self.loop.create_task(self.client._scb_on_privmessage(message))
        elif message.inner == "CommandMessage":
            if message.display_name.lower() != self.nick.lower():
                log.info(f"[CMD].[{message.channel}]: ({message.display_name}) {message.message_text}")
                self.loop.create_task(self.client._scb_on_command(message))

        