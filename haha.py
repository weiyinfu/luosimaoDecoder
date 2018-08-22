import requests
from selenium import webdriver
import time
from pyquery import PyQuery as pq

# 提交表单的地址
submit_url = "http://vote.zazhipu.com/Client/WoDoVote"
# 投票页面的地址
vote_url = "http://vote.zazhipu.com/Home/MagazineDetail/7b655518-2301-4801-bd3a-b47fe5bbb603"
# 火狐驱动的地址
firefox_driverpath = r"C:\Users\weidiao\Downloads\geckodriver-v0.21.0-win64\geckodriver.exe"

sess = requests.session()
driver = webdriver.Firefox(executable_path=firefox_driverpath)
driver.get(vote_url)


def analyze():
    return [(129, 108), (115, 123)]


def get_code():
    act = webdriver.ActionChains(driver)
    act.pause(3)  # 等待加载验证码按钮
    act.move_by_offset(20, 25)
    act.click()
    act.pause(3)  # 等待加载验证码图片
    act.perform()
    print("saving screenshot")
    driver.save_screenshot("haha.png")
    print("analyze")
    positions = analyze()
    print("analyze over", positions)
    for x, y in positions:
        act = webdriver.ActionChains(driver)
        act.move_to_element_with_offset(driver.find_element_by_tag_name("body"), x, y)
        act.click()
        act.perform()
        driver.implicitly_wait(2)
    src = driver.page_source
    html = pq(src)
    code = html("#result").text()
    print("code", code)
    if code:
        print(code)
        submit(code, None)
    else:
        print("破解失败")


get_code()
time.sleep(20)
driver.close()


def submit(code, ip):
    data = {
        "Name": "weiyinfu12",
        "QQ": "1234234343",
        "Email": r"12342434@qq.com",
        "Code": code,
        "Id": "7b655518-2301-4801-bd3a-b47fe5bbb603"
    }
    proxies = dict(http=ip) if ip else None
    resp = sess.post(submit_url, data, proxies=proxies)
    print(resp.text)
