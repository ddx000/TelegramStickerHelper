#!/usr/bin/env python3
import sys
import telepot, telepot.aio
import asyncio, aiofiles
import json
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import ForceReply
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
from random import Random
from scratch import Scratch
import re

# ver0.1

# Please apply for telegram-robot by yourself and get the key
with open('key.json', 'r') as f:
    KEY = json.load(f)['key']

# By using telegram api, uploader must add your robot's name after self.packname
# So change it by yourself
ROBOTNAME = 'TTTTTigeeerBot'


def Random_name(length):
    # Create a certain length random name, for self.packname and self.packtitle
    # If you do mind the name of the stickers, change it for user input
    random_name = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    for i in range(length):
        random_name += chars[Random().randint(0, 51)]
    return random_name


class Stickers(telepot.aio.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(Stickers, self).__init__(*args, **kwargs)
        self.stickeremoji = '😶'
        self.img_bytes = [] # it's the list container for every image after resized (bytes)

    async def open(self, initial_msg,seed):
        # create chat by self.fromid
        self.from_id = initial_msg['from']['id']
        await self.on_chat_message(initial_msg)
        return True

    async def on_chat_message(self, msg):
        """
        this function handles all message user type in
        if it contain http in text, then go to scratch stickers it and upload stickers
        """
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
        print('receive this msg', msg['text'])
        if content_type == 'text' and 'http' in msg['text']:
            url = re.findall(r'(https?://\S+)', msg['text'])[0]
            self.packmade = False
            self.packname = Random_name(10) + '_by_' + ROBOTNAME
            self.packtitle = Random_name(10)
            await self.get_stickers(url)
            await self.uploader()
        return

    async def get_stickers(self, url):
        """call Scratch Module"""
        sc = Scratch(url)
        sc.get_image()
        self.img_bytes = sc.imgBytesLst
        return

    async def uploader(self):
        print('uploader running: ', self.packname)
        for cnt, one_sticker in enumerate(self.img_bytes):
            try:
                if self.packmade:
                    if cnt % 8 == 0: # output progress bar for users
                        progressbar = str((round(cnt / len(self.img_bytes), 2) * 100)) + '%'
                        await self.sender.sendMessage('working: ' + progressbar)
                    await bot.addStickerToSet(self.from_id, self.packname, one_sticker, self.stickeremoji)
                else:  # Create new stickerset, then self.packmade is set to True
                    self.packmade = await bot.createNewStickerSet(self.from_id, self.packname,
                                                                  self.packtitle, one_sticker,
                                                                  self.stickeremoji)
                    await self.sender.sendMessage('Created New StickerSet: ' + self.packname)
            except telepot.exception.TelegramError as e:
                error = str(e)
                print(error)
                await self.sender.sendMessage('something wrong... ' + error)
                break
        await self.sender.sendMessage('Uploaded Finished https://t.me/addstickers/' + self.packname)


bot = telepot.aio.DelegatorBot(KEY, [
    pave_event_space()(per_chat_id(), create_open, Stickers, timeout=70 * 1300), ])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Start Telegram Bot')
loop.run_forever()
