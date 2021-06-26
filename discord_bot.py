import asyncio
import discord
from discord.ext import commands
import json
import requests
from bs4 import BeautifulSoup
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="[", intents=intents)

with open("setting.json", "r", encoding="utf8") as setting_file:
    setting = json.load(setting_file)

@bot.event
async def on_ready():
    print("==============================\n")
    print("Discord 機器人已成功上線\n")
    print("==============================\n")

@bot.command()
async def hi(ctx):
    if ctx.message.author.id == setting["廖廢物id"]:
        await ctx.send("有叫你玩我嗎?")
    else:
        await ctx.send("喵喵喵~ Hello, {}".format(ctx.message.author.name))

@bot.command()
async def del_msg(ctx, times: int):
    if ctx.message.author.id == setting["江恩id"]:
        if 1 <= times <= 99:
            times = times + 1
            await ctx.channel.purge(limit=times)
        else:
            await ctx.send("$del_msg 數量\n")
    else:
        await ctx.send("你沒有權限使用此指令")

# This is a Web Crawler to get FCU information.
async def send_message():
    await bot.wait_until_ready()
    send_msg_channel = bot.get_channel(847039097238192140)

    while not bot.is_closed():
        current_time = time.localtime()
        current_time = int(time.strftime("%H", current_time))

        if 9 <= current_time <= 17:
            target_web = requests.get("https://www.fcu.edu.tw/national_list/110college_transfer/")
            soup = BeautifulSoup(target_web.text, "html.parser")
            title = soup.find_all("a", class_="a-news-list__title")

            with open("check_file.txt", "r", encoding="utf-8") as cf:
                check_file = cf.readlines()

            for i in range(len(check_file)):
                check_file[i] = check_file[i].strip()

            for i in range(len(title) - 1, -1, -1):
                if title[i].string not in check_file:
                    with open("check_file.txt", "a+", encoding="utf-8") as cf_write:
                        cf_write.write(str(title[i].string) + "\n")
                    await send_msg_channel.send(title[i].string)

        await asyncio.sleep(3600)

bot.loop.create_task(send_message())
bot.run(setting["token"])
