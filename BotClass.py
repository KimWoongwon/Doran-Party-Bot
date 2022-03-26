import datetime, copy
from EmojiSet import *
from Excptions import *
from partyinfo import *
from replit import db


class Bot:
    prefix = '!봇'

    days = ['월', '화', '수', '목', '금', '토', '일']
    updateKeys = ['시간', '요일', '레이드', '난이도', '공대장', '제목']
    managerCommand = ["주간리셋", "리셋"]
    memberCommand = ["캘린더", "파티추가", "파티삭제", "파티수정", "멤버추가", "멤버삭제"]

    def __init__(self, prefix) -> None:
        Bot.prefix = prefix

    mon = list()
    tue = list()
    wed = list()
    tur = list()
    fri = list()
    sat = list()
    sun = list()

    daylist = [mon, tue, wed, tur, fri, sat, sun]

    SeedDay = datetime.datetime(2021, 10, 20)
    dtime_wed = SeedDay
    dtime_tue = SeedDay

    editedmsg = ""
    Total_Message = ""

    #region customfunction
    def Get_DaysList(self):
        return Bot.daylist

    def Get_EditMessage(self):
        return Bot.editedmsg

    def Set_EditMessage(self, message):
        if message is not None:
            Bot.editedmsg = message

    def Get_TotalMessage(self):
        return Bot.Total_Message

    def Set_TotalMessage(self, message):
        Bot.Total_Message = message

    def MakePartyMessage(self):
        wednesday = "{0}. {1} ({2})".format(Bot.dtime_wed.month,
                                            Bot.dtime_wed.day,
                                            Bot.days[Bot.dtime_wed.weekday()])
        tuesday = "{0}. {1} ({2})".format(Bot.dtime_tue.month,
                                          Bot.dtime_tue.day,
                                          Bot.days[Bot.dtime_tue.weekday()])

        message =   f"```diff\n" \
                    f"{EmojiSet.seed} 도란 파티 일정표 Beta [{wednesday} ~ {tuesday}] {EmojiSet.seed}\n\n"\
                    f"- {EmojiSet.exclamation} 아직 완벽하지 않으므로 초기화 될 수 있습니다.\n"\
                    f"- {EmojiSet.exclamation} 파티 참여는 '파티' 게시판을 이용해주세요.\n" \
                    f"- {EmojiSet.exclamation} 파티 문의는 해당 파티 공대장에게 부탁드립니다.\n\n"

        for i in range(len(Bot.daylist)):
            temp = (Bot.dtime_wed + datetime.timedelta(days=i))
            message += f"{EmojiSet.calendar} [{temp.day} {Bot.days[temp.weekday()]}]\n"
            for j in range(len(Bot.daylist[temp.weekday()])):
                message += Bot.daylist[temp.weekday()][j].get_infoTostring()

            if len(Bot.daylist[temp.weekday()]) < 3:
                for k in range(0, 3 - len(Bot.daylist[temp.weekday()])):
                    message += "\n\n"

        message += f"\tMade By 프삭, 묘오지\n```"

        Bot.Total_Message = message

    def PrintCommand(self):

        message =   "```diff\n" \
                    " 명령어 목록\n\n"

        message += "- 관리자 명령어\n"
        for item in Bot.managerCommand:
            message += item + "\t"
        message += "\n\n"

        message += "+ 유저 명령어\n"
        for item in Bot.memberCommand:
            message += item + "\t"
        message += "\n"

        message += "```"

        return message

    def PartyInfo_Reset(self):
        partyinfo.index = 0
        for item in Bot.daylist:
            item.clear()

        for key in db.keys():
            del db[key]

    def Week_Reset(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=9)
        delta = (now - Bot.SeedDay) // datetime.timedelta(days=7)

        for i in range(0, delta):
            Bot.SeedDay += datetime.timedelta(days=7)

        Bot.dtime_wed = Bot.SeedDay
        Bot.dtime_tue = Bot.dtime_wed + datetime.timedelta(days=6)

    def Init_days_List(self, item):

        if item.info[Keys.DAY] not in Bot.days:
            raise DaysInputError()

        index = Bot.days.index(item.info[Keys.DAY])
        Bot.daylist[index].append(item)

    def Add_PartyInfo(self, msg, *args):
        partyinfo.Increase_Index()
        index = partyinfo.index
        temp = partyinfo(*args)
        temp.info[Keys.COMMANDER] = msg.author.name

        print(f"Added : {temp.info[Keys.ID]}")

        self.Init_days_List(temp)
        db[temp.info[Keys.ID]] = temp.InfoForDB()

    def Find_PartyInfo_ID(self, id):
        for head in Bot.daylist:
            for item in head:
                if str(item.info[Keys.ID]) == id:
                    return item

        raise IDInputError()

    def Update_PartyInfo(self, *args):
        item = self.Find_PartyInfo_ID(args[0])
        if args[1] not in Bot.updateKeys:
            raise UpdateInputError()

        if args[1] == "시간":
            item.info[Keys.TIME] = args[2]

        elif args[1] == "요일":
            temp = copy.deepcopy(item)
            temp.info[Keys.DAY] = args[2]
            self.Init_days_List(temp)
            self.Delete_PartyInfo_info(item)
            item = temp

        elif args[1] == '레이드':
            item.info[Keys.RAID] = args[2]
            item.info[Keys.EMOJI] = EmojiSet.GetEmoji(args[2])

        elif args[1] == "난이도":
            item.info[Keys.DIFF] = args[2]

        elif args[1] == "제목":
            memo = ""
            for i in range(2, len(args)):
                memo += args[i] + " "

            item.info[Keys.MEMO] = memo

        elif args[1] == "공대장":
            item.info[Keys.COMMANDER] = args[2]

        db[args[0]] = item.InfoForDB()

    def Delete_PartyInfo(self, id):
        for head in Bot.daylist:
            for item in head:
                if str(item.get_id()) == id:
                    head.remove(item)
                    del db[id]
                    return None

        raise IDInputError()

    def Delete_PartyInfo_info(self, info):
        for head in Bot.daylist:
            for item in head:
                if item == info:
                    head.remove(item)
                    return None

    def Add_Member(self, *args):
        item = self.Find_PartyInfo_ID(args[0])

        if args[1] == "딜":
            DCOUNT = int(item.info[Keys.DCOUNT]) + 1
            item.info[Keys.DCOUNT] = DCOUNT
        elif args[1] == "폿" or args[1] == '힐':
            HCOUNT = int(item.info[Keys.HCOUNT]) + 1
            item.info[Keys.HCOUNT] = HCOUNT
        else:
            return
        temp = dict()
        temp[args[2]] = args[1]
        item.info[Keys.MEMBERS].append(temp)
        db[args[0]] = item.InfoForDB()

    def Delete_Member(self, *args):
        item = self.Find_PartyInfo_ID(args[0])

        for member in item.info[Keys.MEMBERS]:
            if args[1] in member.keys():
                if member[args[1]] == "딜":
                    if int(item.info[Keys.DCOUNT]) > 0:
                        DCOUNT = int(item.info[Keys.DCOUNT]) - 1
                        item.info[Keys.DCOUNT] = DCOUNT
                elif member[args[1]] == "폿" or member[args[1]] == '힐':
                    if int(item.info[Keys.HCOUNT]) > 0:
                        HCOUNT = int(item.info[Keys.HCOUNT]) - 1
                        item.info[Keys.HCOUNT] = HCOUNT
                else:
                    return
                item.info[Keys.MEMBERS].remove(member)

        db[args[0]] = item.InfoForDB()

    #endregion
