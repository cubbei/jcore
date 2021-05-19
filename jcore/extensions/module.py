import jcore
from jcore.message import *

class Module():

    def on_raw(self, data: RawMessage, socket: jcore.jsocket.Socket): 
        """Invoked when a RawMessage message is sent to the bot."""
        pass

    def on_join(self, data: Join, socket: jcore.jsocket.Socket): 
        """Invoked when a Join message is sent to the bot."""
        pass

    def on_part(self, data: Part, socket: jcore.jsocket.Socket): 
        """Invoked when a Part message is sent to the bot."""
        pass

    def on_mode(self, data: Mode, socket: jcore.jsocket.Socket): 
        """Invoked when a Mode message is sent to the bot."""
        pass

    def on_names(self, data: Names, socket: jcore.jsocket.Socket): 
        """Invoked when a Names message is sent to the bot."""
        pass

    def on_clearchat(self, data: ClearChat, socket: jcore.jsocket.Socket): 
        """Invoked when a ClearChat message is sent to the bot."""
        pass

    def on_clearmessage(self, data: ClearMessage, socket: jcore.jsocket.Socket): 
        """Invoked when a ClearMessage message is sent to the bot."""
        pass

    def on_hosttarget(self, data: HostTarget, socket: jcore.jsocket.Socket): 
        """Invoked when a HostTarget message is sent to the bot."""
        pass

    def on_notice(self, data: Notice, socket: jcore.jsocket.Socket): 
        """Invoked when a Notice message is sent to the bot."""
        pass

    def on_reconnect(self, data: Reconnect, socket: jcore.jsocket.Socket): 
        """Invoked when a Reconnect message is sent to the bot."""
        pass

    def on_roomstate(self, data: RoomState, socket: jcore.jsocket.Socket): 
        """Invoked when a RoomState message is sent to the bot."""
        pass

    def on_userstate(self, data: UserState, socket: jcore.jsocket.Socket): 
        """Invoked when a UserState message is sent to the bot."""
        pass

    def on_globaluserstate(self, data: GlobalUserState, socket: jcore.jsocket.Socket): 
        """Invoked when a GlobalUserState message is sent to the bot."""
        pass

    def on_privmessage(self, data: PrivateMessage, socket: jcore.jsocket.Socket): 
        """Invoked when a PrivateMessage message is sent to the bot."""
        pass

    def on_usernotice(self, data: UserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a UserNotice message is sent to the bot."""
        pass

    def on_ritual_usernotice(self, data: RitualUserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a RitualUserNotice message is sent to the bot."""
        pass

    def on_bitbadgeupgrade_usernotice(self, data: BitBadgeUpgradeUserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a BitBadgeUpgradeUserNotice message is sent to the bot."""
        pass

    def on_raid_usernotice(self, data: RaidUserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a RaidUserNotice message is sent to the bot."""
        pass

    def on_subscriber_usernotice(self, data: SubscriberUserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a SubscriberUserNotice message is sent to the bot."""
        pass

    def on_giftedsubscriber_usernotice(self, data: GiftedSubscriberUserNotice, socket: jcore.jsocket.Socket): 
        """Invoked when a GiftedSubscriberUserNotice message is sent to the bot."""
        pass

    def on_whisper(self, data: Whisper, socket: jcore.jsocket.Socket): 
        """Invoked when a Whisper message is sent to the bot."""
        pass

    def on_command(self, data: CommandMessage, socket: jcore.jsocket.Socket): 
        """Invoked when a CommandMessage message is sent to the bot."""
        pass


    def setup(self, client: jcore.Client):
        raise NotImplementedError()
        #client.log.debug(f"Loaded Command {self.name}")

    def teardown(self, client: jcore.Client):
        raise NotImplementedError()
        #client.log.debug(f"Removed Command {self.name}")


