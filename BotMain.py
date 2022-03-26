import asyncio
import discord, os
from discord.ext import commands, tasks
import EmojiSet
from keep_alive import keep_alive
from BotClass import *
from Excptions import *

app = commands.Bot(command_prefix='!봇 ')
bot = Bot('!봇')

ManagerRole = "임원회"+emoji.emojize(":crown:")
ProgramerRole = "관리자"+emoji.emojize(":fleur-de-lis:")
guild_ID = int(os.environ['GID'])
channel_ID = int(os.environ['CID'])

def loaded_from_db(*args):
        print(*args)
        tempargs = (args[0], args[1], args[2], args[3], args[4])
        tempitem = partyinfo(*tempargs)

        tempitem.info[Keys.DCOUNT] = args[5]
        tempitem.info[Keys.HCOUNT] = args[6]
        tempitem.info[Keys.COMMANDER] = args[7]
        
        for i in range(8, len(args), 2):
            temp = dict()
            temp[args[i + 1]] = args[i]
            tempitem.info[Keys.MEMBERS].append(temp)

        return tempitem

def LoadFromDB():
    for key in db.keys():
        print(key, end=" ")
        args = db[key].split('_')
        item = loaded_from_db(*args)
        item.info[Keys.ID] = int(key)
        if partyinfo.index < int(key):
            partyinfo.index = int(key)
        bot.Init_days_List(item)

    print(f"Current ID : {partyinfo.index}")

    

async def SendCalender():
    if bot.Get_EditMessage() == "":
        bot.Set_EditMessage(await app.get_guild(guild_ID).get_channel(channel_ID).send(bot.Get_TotalMessage()))
    else:
        await bot.Get_EditMessage().edit(content=bot.Get_TotalMessage())

async def ErrorEmbed(ctx, err):
    embed = discord.Embed(title = f"Error{EmojiSet.exclamation}", description=f"{err}", color=discord.Color.red())
    errmsg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await errmsg.delete()

@app.event
async def on_ready():
    print("login")
    print(app.user.name)
    print(app.user.id)
    print("--------------------------")
    
    messagelist = await app.get_guild(guild_ID).get_channel(channel_ID).history(limit=None).flatten()
    for message in messagelist:
        if message is None:
            break
        await message.delete()

    await app.get_guild(guild_ID).get_channel(channel_ID).send(bot.PrintCommand())

    if len(db.keys()) == 0:
        bot.PartyInfo_Reset()
    else:
        LoadFromDB()

    bot.Week_Reset()
    bot.MakePartyMessage()

    await SendCalender()
    await app.change_presence(status = discord.Status.online, activity = discord.Game('파티 관리'))


@app.command(name="주간리셋")
async def Weekend_Reset(ctx):
    print("명령어 : {0}".format("주간리셋"))
    global ManagerRole
    global ProgramerRole
    try:
        usermessage = ctx.message
        rolelist = []
        for role in ctx.author.roles:
            rolelist.append(role.name)

        if ManagerRole in rolelist or ProgramerRole in rolelist:
            bot.PartyInfo_Reset()
            bot.Week_Reset()
            bot.MakePartyMessage()

            await SendCalender()   

        else:
            raise ManagerError()
                
    except ManagerError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

@app.command(name="리셋")
async def Reset(ctx):
    global ManagerRole
    print("명령어 : {0}".format("리셋"))
    try:
        usermessage = ctx.message
        rolelist = []
        for role in ctx.author.roles:
            rolelist.append(role.name)

        if ManagerRole in rolelist or ProgramerRole in rolelist:
            bot.PartyInfo_Reset()
            bot.MakePartyMessage()
            await SendCalender()

        else:
            raise ManagerError()
                
    except ManagerError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

@app.command(name="파티추가")
async def ADD(ctx, *args):
    print("명령어 : {0}, {1}".format("파티추가", args))
    try:
        usermessage = ctx.message
        if len(args) < 5:
            raise ParamError()
        
        bot.Add_PartyInfo(ctx, *args)
        bot.MakePartyMessage()
        await SendCalender()

    except ParamError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

@app.command(name="파티삭제")
async def DELETE(ctx, *args):
    print("명령어 : {0}, {1}".format("파티삭제", args))
    try:
        usermessage = ctx.message
        bot.Delete_PartyInfo(args[0])
        bot.MakePartyMessage()

        await SendCalender()

    except IDInputError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

@app.command(name="파티수정")
async def UPDATE(ctx, *args):
    print("명령어 : {0}, {1}".format("파티수정", args))
    try:
        usermessage = ctx.message
        bot.Update_PartyInfo(*args)
        bot.MakePartyMessage()

        await SendCalender()

    except UpdateInputError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

@app.command(name="멤버추가")
async def UPDATE(ctx, *args):
    print("명령어 : {0}, {1}".format("멤버추가", args))
    try:
        usermessage = ctx.message
        bot.Add_Member(*args)
        bot.MakePartyMessage()

        await SendCalender()

    except UpdateInputError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()
    
@app.command(name="멤버삭제")
async def UPDATE(ctx, *args):
    print("명령어 : {0}, {1}".format("멤버삭제", args))  
    try:
        usermessage = ctx.message
        bot.Delete_Member(*args)
        bot.MakePartyMessage()

        await SendCalender()

    except UpdateInputError as err:
        await ErrorEmbed(ctx, err)
    finally:
        await usermessage.delete()

keep_alive()
my_secret = os.environ['BOT_TOKEN']
app.run(my_secret)


