import emoji

class EmojiSet:
    seed = emoji.emojize(":seedling:")
    exclamation = emoji.emojize(":red_exclamation_mark:")
    calendar = emoji.emojize(":spiral_calendar:")
    sword = emoji.emojize(":crossed_swords:")
    healer = emoji.emojize(":syringe:")
    person = emoji.emojize(":bust_in_silhouette:")
    bal = emoji.emojize(":cow_face:")
    via = emoji.emojize(":kiss_mark:")
    cuc = emoji.emojize(":clown_face:")
    ave = emoji.emojize(":crystal_ball:")
    argos = emoji.emojize(":unicorn:")
    dogato = emoji.emojize(":fox:")
    dovis = emoji.emojize(":fleur-de-lis:")
    others = emoji.emojize(":small_orange_diamond:")

    @classmethod
    def GetEmoji(cls, raid):
        if raid == "발탄":
            return cls.bal
        elif raid in "비아키스" or raid in "비아":
            return cls.via
        elif raid in "쿠크세이튼" or raid in "쿠크":
            return cls.cuc
        elif raid == "아브렐슈드" or raid in "아브":
            return cls.ave
        elif raid == "아르고스":
            return cls.argos
        elif raid == "도전어비스던전" or raid == "도비스":
            return cls.dovis
        elif raid == "도전가디언토벌" or raid == "도가토":
            return cls.dogato
        else:
            return cls.others
