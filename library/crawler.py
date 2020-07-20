import requests, os, time, datetime, psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawling_lib():
    chrome_options = webdriver.ChromeOptions()
    try:
        # chrome_options.binary_location = "/usr/bin/brave-browser"
        driver = webdriver.Chrome('/home/jil8885/Downloads/chromedriver', options=chrome_options)
    except:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    

    # ERICA Campus
    request_url = "https://information.hanyang.ac.kr/#/smuf/seat/status"
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    driver.get(request_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ikc-container.ng-scope > div.ikc-content > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > span:nth-child(2)")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.findAll("span", {"ng-bind": "s.name"})
        total = soup.findAll("span", {"ng-bind": "s.activeTotal"})
        active = soup.findAll("span", {"ng-bind": "s.occupied"})
        percent = soup.findAll("span", {"ng-bind": "s.rate + '%'"})
        conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
        conn = psycopg2.connect(conn_sql)
        cursor = conn.cursor()
        cursor.execute("drop table if exists libinfo")
        cursor.execute("drop table if exists time")
        cursor.execute("CREATE TABLE libinfo(name text, total int, occupied int, percent text)")
        cursor.execute("CREATE TABLE time(month int, day int, hour int, min int)")
        for x in range(len(name)):
            sql = "INSERT INTO libinfo(name, total, occupied, percent) values (%s, %s, %s, %s)"
            # print((name[x].text, int(total[x].text), int(active[x].text), percent[x].text))
            cursor.execute(sql, (name[x].text, int(total[x].text), int(active[x].text), percent[x].text))
            conn.commit()
        sql = "INSERT INTO time (month, day, hour, min) values (%s, %s, %s, %s)"
        cursor.execute(sql, (int(now.month), int(now.day), int(now.hour), int(now.minute)))
        conn.commit()
        cursor.close()
        conn.close()
    finally:
        # driver.close()
        pass

    # Seoul Campus
    request_url = "https://library.hanyang.ac.kr/#/smuf/seat/status"
    driver.get(request_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ikc-content > div > div > div > div > table > tbody > tr:nth-child(1) > td.ikc-seat-name > span:nth-child(2)")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.findAll("span", {"ng-bind": "s.name"})
        total = soup.findAll("span", {"ng-bind": "s.activeTotal"})
        active = soup.findAll("span", {"ng-bind": "s.occupied"})
        percent = soup.findAll("span", {"ng-bind": "s.rate + '%'"})
        conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
        conn = psycopg2.connect(conn_sql)
        cursor = conn.cursor()
        for x in range(len(name)):
            sql = "INSERT INTO libinfo(name, total, occupied, percent) values (%s, %s, %s, %s)"
            # print((name[x].text, int(total[x].text), int(active[x].text), percent[x].text))
            cursor.execute(sql, (name[x].text, int(total[x].text), int(active[x].text), percent[x].text))
            conn.commit()
        sql = "INSERT INTO time (month, day, hour, min) values (%s, %s, %s, %s)"
        cursor.execute(sql, (int(now.month), int(now.day), int(now.hour), int(now.minute)))
        conn.commit()
        cursor.close()
        conn.close()
    finally:
        driver.close()
        driver.quit()
    return

crawling_lib()