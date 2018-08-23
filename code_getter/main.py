import time

from pyquery import PyQuery as pq
from selenium import webdriver
import os
from code_recognizer import human_recognizer

"""
天亡我也，非战之罪也。

版本问题太多了，总是出现莫名其妙的错误：

不做了

  File "C:\anaconda\lib\http\client.py", line 297, in begin
    version, status, reason = self._read_status()
  File "C:\anaconda\lib\http\client.py", line 258, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
  File "C:\anaconda\lib\socket.py", line 575, in readinto
    return self._sock.recv_into(b)
ConnectionAbortedError: [WinError 10053] 你的主机中的软件中止了一个已建立的连接。
"""
# 投票页面的地址

vote_url = "http://vote.zazhipu.com/Home/MagazineDetail/7b655518-2301-4801-bd3a-b47fe5bbb603"

# 火狐驱动的地址
firefox_driverpath = r"C:\Users\weidiao\Downloads\geckodriver-v0.21.0-win64\geckodriver.exe"
# chrome_driverpath = r"C:\Users\weidiao\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Firefox(executable_path=firefox_driverpath)
# driver = webdriver.Chrome(chrome_driverpath)
driver.get(vote_url)


def analyze():
    return human_recognizer.recognize()


def get_code():
    time.sleep(3)
    act = webdriver.ActionChains(driver)
    act.move_by_offset(20, 25).click().perform()
    time.sleep(3)
    print("saving screenshot")
    driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "resource", "haha.png"))
    print("analyze")
    positions = analyze()
    print("analyze over", positions)
    for x, y in positions:
        act.reset_actions()
        # 把body的style设置为占满全部空间，margin设置为0，则可以去往任意位置矣
        act.move_to_element_with_offset(driver.find_element_by_tag_name("body"), x, y)
        act.click()
        act.perform()
        time.sleep(3)
    src = driver.page_source
    # print(src)
    html = pq(src)
    code = html("#result").text()
    print("create_code", code)
    if code:
        print(code)
        submit(code, None)
    else:
        print("破解失败")


get_code()
time.sleep(20)
driver.close()
