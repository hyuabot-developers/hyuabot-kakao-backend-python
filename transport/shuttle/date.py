# 오늘이 학기 중인지, 주말인지 구별하는 코드
def is_semester(month, day):
    semester = [4, 9, 10, 11]
    vacation = [1, 2, 5, 7, 8]
    # return False
    if month in semester:
        return True
    elif month in vacation:
        return False
    elif month == 3:
        if day < 28:
            return False
        else:
            return True
    else:
        if day < 22:
            return True
        else:
            return False


def is_seasonal(month, day):
    # 2020 plan
    if ((month == 6 and day > 21) or (month == 7 and day < 15)) or (
            (month == 12 and day > 23) or (month == 1 and day < 16)):
        return True
    else:
        return False
