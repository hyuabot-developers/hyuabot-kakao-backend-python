import requests, os, time, psycopg2
from bs4 import BeautifulSoup


def crawling_lib(location = None):
    conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
    conn = psycopg2.connect(conn_sql)
    cursor = conn.cursor()
    string = ""
    sql = "select * from time"
    cursor.execute(sql)
    time = cursor.fetchone()
    string += str(time[0]) + "월" + str(time[1]) + "일" + str(time[2]) + "시" + str(time[3]) + "분 기준\n" 
    sql = "select * from libinfo"
    cursor.execute(sql)
    libinfo = cursor.fetchall()
    if location == 0:
        for x in libinfo[:4]:
            string += x[0] + " "
            totalseat = int(x[1])
            activeseat = int(x[2])
            remained = totalseat - activeseat
            string += "잔여 " + str(remained) + "석\n"
    elif location == 1:
        info = libinfo[0]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 3:
        info = libinfo[1]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 4:
        info = libinfo[2]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 5:
        info = libinfo[3]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    cursor.close()
    conn.close()
    return string.strip()

def crawling_lib2(location = None):
    conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
    conn = psycopg2.connect(conn_sql)
    cursor = conn.cursor()
    string = ""
    sql = "select * from time"
    cursor.execute(sql)
    time = cursor.fetchone()
    string += str(time[0]) + "월" + str(time[1]) + "일" + str(time[2]) + "시" + str(time[3]) + "분 기준\n" 
    sql = "select * from libinfo"
    cursor.execute(sql)
    libinfo = cursor.fetchall()
    if location == 0:
        for x in libinfo[4:]:
            string += x[0] + " "
            totalseat = int(x[1])
            activeseat = int(x[2])
            remained = totalseat - activeseat
            string += "잔여 " + str(remained) + "석\n"
    elif location == 1:
        info = libinfo[-4]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 2:
        info = libinfo[-3]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 3:
        info = libinfo[-2]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 4:
        info = libinfo[-1]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 5:
        info = libinfo[4]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 6:
        info = libinfo[5]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 7:
        info = libinfo[6]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    elif location == 8:
        info = libinfo[7]
        string += info[0] + "\n"
        string += "총 좌석:" + str(info[1]) + "석\n"
        string += "사용중:" + str(info[2]) + "석\n"
        remained = info[1] - info[2]
        string += "잔여좌석:" + str(remained) + "석\n"
        string += "점유율:" + str(info[3]) + "\n"
    cursor.close()
    conn.close()
    return string.strip()
