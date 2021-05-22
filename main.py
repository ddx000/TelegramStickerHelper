import asyncio
import json
import re
import telepot, telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space

from crawler.scratch_tool import get_sticker_name_hash
from crawler.line_crawler import LineCrawler

"""
pipenv run python ./TeleRobot.py
"""


"""
Please apply for telegram-robot by yourself and get the key
By using telegram api, uploader must add your robot's name after self.packname
So change it by yourself
"""
with open('key.json', 'r') as f:
    key = json.load(f)
    TOKEN = key['RobotToken']
    ROBOTNAME = key['RobotName']


class TelegramRobot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramRobot, self).__init__(*args, **kwargs)
        self.stickeremoji = '😶'

    async def open(self, initial_msg,seed):
        """ Every msg from each users need a connection open, return True if session created"""
        self.from_id = initial_msg['from']['id']
        await self.on_chat_message(initial_msg)
        return True

    async def on_chat_message(self, msg):
        """this function handles all message user type in
        if it contain http in text, then go to scratch stickers it and upload stickers"""

        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)

        if content_type == 'text' and 'http' in msg['text']:
            url = re.findall(r'(https?://\S+)', msg['text'])[0]
            self.packmade = False
            img_bytes = LineCrawler.get_sticker_resized_bytes(url)
            line_sticker_name = LineCrawler.get_sticker_name(url)
            telegram_package_name = get_sticker_name_hash(line_sticker_name)
            await self.uploader(img_bytes, telegram_package_name, line_sticker_name )

        if content_type == 'text' and 'dev_test' in msg['text']:
            self.packmade = False
            await self.uploader(LineCrawler().get_test_imgbytes(),'00001', 'title')



    async def uploader(self, imgbytelst, sticker_id, title):
        packname = sticker_id +'_by_' + ROBOTNAME
        print('Uploader running: ', packname)
        for cnt, one_sticker in enumerate(imgbytelst):
            print(cnt, one_sticker)
            try:
                if self.packmade:
                    if cnt % 8 == 0: # output progress bar for users
                        progressbar = str((round(cnt / len(imgbytelst), 2) * 100)) + '%'
                        await self.sender.sendMessage('working: ' + progressbar)
                    await bot.addStickerToSet(self.from_id, packname, one_sticker, self.stickeremoji)
                else:  # Create new stickerset, then self.packmade is set to True
                    self.packmade = await bot.createNewStickerSet(self.from_id, packname,
                                                                  title, one_sticker,
                                                                  self.stickeremoji)
                    await self.sender.sendMessage('Created New StickerSet: ' + packname)
            except telepot.exception.TelegramError as e:
                if 'sticker set name is already occupied' in str(e):
                    await self.sender.sendMessage('Already Uploaded')
                else:
                    await self.sender.sendMessage('something wrong... ' + str(e))
                break
        await self.sender.sendMessage('Uploaded Finished https://t.me/addstickers/' + packname)

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(per_chat_id(), create_open, TelegramRobot, timeout=60 * 60* 12), ])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Start Telegram Bot')
loop.run_forever()
