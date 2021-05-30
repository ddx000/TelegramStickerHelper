import asyncio
import json
import re
import logging as log

import telepot, telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space

from crawler.scratch_tool import get_sticker_name_hash
from crawler.line_crawler import LineCrawler

"""
pipenv run python ./main.py
"""

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[log.FileHandler("debug.log"), log.StreamHandler()],
)

# Please apply for telegram-robot by yourself and get the key
with open("key.json", "r") as f:
    key = json.load(f)
    TOKEN = key["RobotToken"]
    ROBOTNAME = key["RobotName"]


class TelegramRobot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramRobot, self).__init__(*args, **kwargs)
        self.stickeremoji = "😶"
        self.upload_success = 0
        self.upload_fail = 0

    async def open(self, initial_msg, seed):
        """Every msg from each users need a connection open, return True if session created"""
        self.from_id = initial_msg["from"]["id"]
        await self.on_chat_message(initial_msg)
        return True

    async def on_chat_message(self, msg):
        """this function handles all message user type in
        if it contain http in text, then go to scratch stickers it and upload stickers"""

        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(
            msg, long=True
        )
        try:
            if content_type == "text" and "http" in msg["text"]:
                url = re.findall(r"(https?://\S+)", msg["text"])[0]
                img_bytes = LineCrawler.get_sticker_resized_bytes(url)
                line_sticker_name = LineCrawler.get_sticker_name(url)
                telegram_package_name = get_sticker_name_hash(line_sticker_name)
                await self.uploader(img_bytes, telegram_package_name, line_sticker_name)

            elif content_type == "text" and "debug" in msg["text"]:
                await self.sender.sendMessage(f"Robot alive SUCCESS:{self.upload_success} FAIL: {self.upload_fail}")
        except Exception as ex:
            await self.sender.sendMessage("Something wrong...on_chat_message  " + str(ex))
            log.exception(f"Something wrong on_chat_message -{ex}")
            msg_text = msg["text"]
            log.error(f"{content_type} -msg - {msg_text}")
            log.info(f"{chat_type} {chat_id} {msg_date} {msg_id}")
            self.upload_fail += 1


    async def uploader(self, imgbytelst, sticker_id, title):
        packname = sticker_id + "_by_" + ROBOTNAME
        log.info(f"Uploader running:{packname} - {title}")
        await self.sender.sendMessage(f"Uploader running:{title}")
        # DON'T USE asyncio.wait(tasks) here, will cause send a lot of requests in a shorttime
        # and get 429 Requests too many here
        # so here we still just use sync for loop

        for cnt, one_sticker in enumerate(imgbytelst):
            try:
                if cnt == 0:
                    # Create new stickerset
                    log.info(f"Create New Sticker Set")
                    create_success = await bot.createNewStickerSet(
                        self.from_id, packname, title, one_sticker, self.stickeremoji
                    )
                    if create_success:
                        log.info(
                            f"Create New Sticker Set {packname} - {title}  success"
                        )
                        await self.sender.sendMessage(
                            "Created New StickerSet: " + packname
                        )
                    else:
                        log.error(f"Created New StickerSet {packname} - {title} Failed")
                        await self.sender.sendMessage("Created New StickerSet Failed")
                elif cnt > 0:
                    if cnt % 8 == 0:  # output progress bar for users
                        progressbar = str((round(cnt / len(imgbytelst), 2) * 100)) + "%"
                        log.info(f"{packname} - {title} In progess - {progressbar}")
                        await self.sender.sendMessage("Working: " + progressbar)
                    await bot.addStickerToSet(
                        self.from_id, packname, one_sticker, self.stickeremoji
                    )
            except telepot.exception.TelegramError as e:
                if "sticker set name is already occupied" in str(e):
                    await self.sender.sendMessage("Already Uploaded")
                    await self.sender.sendMessage(
                        "Try to find it here https://t.me/addstickers/" + packname
                    )
                    log.warning(
                        f"{title} Already Uploaded -https://t.me/addstickers/{packname}"
                    )
                else:
                    await self.sender.sendMessage("Something wrong... " + str(e))
                    log.exception(f"{title}-{packname} Something wrong -{e}")
                    self.upload_fail += 1
                break
            except Exception as e:
                await self.sender.sendMessage("Something wrong... " + str(e))
                log.exception(f"{title}-{packname} Something wrong -{e}")
                self.upload_fail += 1
                break
        else:
            await self.sender.sendMessage(
                "Uploaded Finished https://t.me/addstickers/" + packname
            )
            self.upload_success +=1
            log.info(f"{packname} - {title} Finish")


bot = telepot.aio.DelegatorBot(
    TOKEN,
    [
        pave_event_space()(
            per_chat_id(), create_open, TelegramRobot, timeout=60 * 60 * 12
        ),
    ],
)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
log.info("Starting")
loop.run_forever()
