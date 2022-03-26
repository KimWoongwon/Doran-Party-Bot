from EmojiSet import EmojiSet
from Excptions import RaidInputError
from GlobalValues import Keys

class partyinfo:
    index = 0


    def __init__(self, *args):
        self.info = dict()
        
        self.info[Keys.ID] = partyinfo.index
        self.info[Keys.DAY] = args[0]
        self.info[Keys.TIME] = args[1]
        self.info[Keys.RAID] = args[2]
        self.info[Keys.DIFF] = args[3]

        memo = ""
        for i in range(4, len(args)):
            memo += f"{args[i]}"
        self.info[Keys.MEMO] = memo

        self.info[Keys.EMOJI] = EmojiSet.GetEmoji(self.info[Keys.RAID])
        self.info[Keys.COMMANDER] = "수정요망"
        self.info[Keys.DCOUNT] = 0
        self.info[Keys.HCOUNT] = 0
        self.info[Keys.MEMBERS] = list()

    def get_infoTostring(self):
        message = f"- ID : {self.info[Keys.ID]}\n"

        if self.info[Keys.DIFF] == '하드' or self.info[Keys.DIFF] == '헬':
            message += "- "
        else:
            message += "+ "

        message +=  f"<{self.info[Keys.TIME]}> {self.info[Keys.EMOJI]} {self.info[Keys.RAID]} {self.info[Keys.DIFF]} {self.info[Keys.MEMO]}\n" \
                    f" {EmojiSet.sword} {self.info[Keys.DCOUNT]} {EmojiSet.healer} {self.info[Keys.HCOUNT]}\n" \
                    f" {EmojiSet.person} 공대장 : {self.info[Keys.COMMANDER]}\n"

        message += f"--- "

        for item in self.info[Keys.MEMBERS]:
            for key in item.keys():
                if item[key] == '딜':
                    message += EmojiSet.sword
                else:
                    message += EmojiSet.healer
                message += key + ", "

        message += "\n\n"

        return  message

    def get_id(self):
        return self.info[Keys.ID]

    def InfoForDB(self):
        message = f"{self.info[Keys.DAY]}_{self.info[Keys.TIME]}_{self.info[Keys.RAID]}_"\
                  f"{self.info[Keys.DIFF]}_{self.info[Keys.MEMO]}_{self.info[Keys.DCOUNT]}_{self.info[Keys.HCOUNT]}_"\
                  f"{self.info[Keys.COMMANDER]}"

        for member in self.info[Keys.MEMBERS]:
            for key in member.keys():
                message += f"_{member[key]}"
                message += f"_{key}"

        return message

    @classmethod
    def Increase_Index(cls):
        cls.index += 1