# 오늘이 학기 중인지, 주말인지 구별하는 코드
def is_semester(month, day):
    semester = [3, 4, 5, 9, 10, 11]
    vacation = [1, 2, 7, 8]
    if month in semester:
        return True
    elif month in vacation:
        return False
    else:
        if day < 22:
            return True
        else:
            return False