

**Disclaimer: It is illegal to upload copyrighted stickers to telegram, please use at your own risk**
1. This code is for academic use only, you can learn python, asyncio, web crawler and API integration from it
2. It is mentioned in Telegram's usage specifications that stickers cannot upload copyrighted things, so it is illegal to crawl Line stickers arbitrarily, and you are responsible for the consequences.

# Telegram Sticker Helper v 1.2
Telegram Sticker Helper is an Sticker Bot for the Telegram Messenger.
Which has the ability for crawler different sources image and automatically upload to telegram sticker API.


# How to setup Enviroment
```git clone https://github.com/ddx000/LineStickers_toTelegram.git```
```pipenv install```

# how to run test
```pipenv run python -m pytest -s```

# how to get telegram bot credentials
Use telegram to create a robot first [Turtorial](https://medium.com/%E8%AA%A4%E9%97%96%E6%95%B8%E6%93%9A%E5%8F%A2%E6%9E%97%E7%9A%84%E5%95%86%E7%AE%A1%E4%BA%BAzino/telegram%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA%E8%B6%85%E8%A9%B3%E7%B4%B0%E6%87%B6%E4%BA%BA%E5%8C%85-%E5%95%86%E7%AE%A1%E4%BA%BA%E9%83%BD%E7%9C%8B%E5%BE%97%E6%87%82-%E9%99%84python%E7%A8%8B%E5%BC%8F%E7%A2%BC-1ec81a91ce48)  
In the same folder, please create key.json by yourself. The content example is as follows:
```
{"RobotToken": "Your robot TOKEN",
"RobotName": "Your robot Name"}
```

# how to run main program?
```pipenv run python ./main.py```


## Demo
Send the sticker website's url to the robot, then the bot will automatic scratch all the stickers images, and upload as one sticker set.  
![](https://i.imgur.com/ob3Eqbe.png)
paste the url on chat windows and then you will get stickers


## TODO
- support animate stickers (WIP)
- support multiple source (Let me know if need another source)
- change crawler to aiohttps.request

## Known restriction
-  DON'T try to speed up uploading with asyncio.wait(tasks)
-  for calling upload API in telegram, there is a rate limit and send many requests in a shorttime will get 429 error code


## Change Logs

### 1.2
2021/5/22
- Refactor all structure (with Class, Folder)
- Change unittest to pytest
- fix crawler issue
- Decoupling some function

### 1.1
2020/7/4  
- Refactor backend code
- Fixed crawler issues(Sync)  
- added unittest  

### 1.0
2020/4/14
- First Commit  





