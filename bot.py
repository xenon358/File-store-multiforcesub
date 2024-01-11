from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client, enums
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_GROUP, CHANNEL_ID, PORT, OWNER

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}\n——"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot stopped. Join the group https://t.me/Bihari_Anime for assistance."
            )
            sys.exit()

        if FORCE_SUB_CHANNEL:
            try:
                info = await self.get_chat(FORCE_SUB_CHANNEL)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = info.invite_link
                self.invitelink = link
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_CHANNEL detected!\n┌ Title: {info.title}\n└ Chat ID: {info.id}\n——"
                )
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bots cannot Retrieve invite links from FORCE_SUB_CHANNEL!"
                )
                self.LOGGER(__name__).warning(
                    f"Ensure that @{self.username} is an admin in the mentioned Channel. Current F-Subs Channel Chat ID: {FORCE_SUB_CHANNEL}"
                )
                self.LOGGER(__name__).info(
                    "Bot stopped. Join the group https://t.me/Bihari_Anime for assistance."
                )
                sys.exit()

        if FORCE_SUB_GROUP:
            try:
                info = await self.get_chat(FORCE_SUB_GROUP)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_GROUP)
                    link = info.invite_link
                self.invitelink2 = link
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_GROUP detected!\n┌ Title: {info.title}\n└ Chat ID: {info.id}\n——"
                )
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot unable to fetch invite link from FORCE_SUB_GROUP!"
                )
                self.LOGGER(__name__).warning(
                    f"Ensure that @{self.username} is an admin in the mentioned Group. Current F-Subs Group Chat ID: {FORCE_SUB_GROUP}"
                )
                self.LOGGER(__name__).info(
                    "Bot stopped. Join the group https://t.me/Bihari_Anime for assistance."
                )
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
            await test.delete()
            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}\n——"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Ensure that @{self.username} is an admin in your Database Channel. Current CHANNEL_ID: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot stopped. Join the group https://t.me/Bihari_Anime for assistance."
            )
            sys.exit()

        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"[🔥 SUCCESSFULLY ACTIVATED! 🔥]\n\nBOT Created by @{OWNER}\nIf @{OWNER} Needs Assistance, Please Ask in the Group https://t.me/Bihari_Anime"
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
