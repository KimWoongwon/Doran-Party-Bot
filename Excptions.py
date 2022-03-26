class ParamError(Exception):
    def __str__(self):
        return "인자값이 너무 많거나 적습니다. (입력 양식을 참고하세요)"
class RaidInputError(Exception):
    def __str__(self):
        return "해당 레이드명이 없습니다. (레이드명 종류를 확인하세요.)"
class DaysInputError(Exception):
    def __str__(self):
        return "요일 입력이 잘못되었습니다."
class CommandNoneError(Exception):
    def __str__(self):
        return "없는 명령어  입니다."
class CommandWError(Exception):
    def __str__(self):
        return "없는 명령어  입니다."
class IDInputError(Exception):
    def __str__(self):
        return "파티 ID가 존재하지 않습니다."
class UpdateInputError(Exception):
    def __str__(self):
        return "업데이트할 항목이 잘못 되었습니다. (입력 양식을 참고하세요)"
class OwnerError(Exception):
    def __str__(self):
        return "파티수정은 공대장만 가능합니다."
class ManagerError(Exception):
    def __str__(self):
        return "관리자 권한이 필요합니다."