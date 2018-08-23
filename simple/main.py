import time
from threading import Thread

from flask import Flask, request, make_response
import requests
from pyquery import PyQuery as pq
from scheduler.main import submit
from proxy_scanner.pycui import pycui
import os
import re

app = Flask(__name__)

codes = []
ips = []
used = set()  # 已经用过的IP
ui = pycui()
mode = "text"  # "crawl"  # 获取IP的模式：爬取（crawl）+从文件读取（text）
test_url = "http://vote.zazhipu.com/"


@app.route("/code/")
def create_code():
    """
    以HTTP接口的形式接受前端发过来的code
    :return:
    """
    code = request.args.get('code')
    print(code)
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.text = "good"
    codes.append(code)
    return resp


def get_code():
    """
    阻塞式获取code
    :return:
    """
    while len(codes) == 0: time.sleep(3)
    code = codes.pop(0)
    return code


def status():
    """
    描述当前队列中的资源个数
    :return:
    """
    ui.info(r"ips {} codes {}".format(len(ips), len(codes)))


def get_ip():
    """
    阻塞式从IP队列中读取
    :return:
    """
    while True:
        status()
        while len(ips) == 0: time.sleep(3)
        ip = ips.pop(0)
        if test_ip(ip):
            return ip


# 从网上免费ip池中，获取ip列表
def crawl_ip():
    """
    从网上下载ip
    :return:
    """
    global ips
    while True:
        try:
            if len(ips) < 100:
                status()
                urls = ["http://www.xicidaili.com/nn",  # 高度匿名
                        # "http://www.xicidaili.com/nt",  # 国内普通代理
                        # "http://www.xicidaili.com/wn",  # 国内HTTPS代理
                        # "http://www.xicidaili.com/wt"# 国内HTTP代理
                        ]
                ans = []
                for i in urls:
                    resp = requests.get(i, headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Host": "www.xicidaili.com",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
                    }, timeout=4)
                    trs = pq(resp.text)("#ip_list tr")
                    for j in range(trs.length):
                        tr = trs.eq(j)
                        tds = tr("td")
                        if len(tds) != 10: continue
                        ip = tds.eq(1).text()
                        port = tds.eq(2).text()
                        ans.append(ip + ":" + port)
                ips = list(set(ips + ans))
            else:
                time.sleep(10)
        except Exception as ex:
            ui.error(ex)


def test_ip(ip):
    """
    测试IP可用性
    :param ip:
    :return:
    """
    ui.info("testing ip {}".format(ip))
    try:
        if ip in used:
            return False
        resp = requests.get(test_url, proxies=dict(http="" if ip.startswith("http") else "http://" + ip), timeout=5)
        ui.info("test result {}".format(resp.status_code))
        return resp.status_code == 200
    except:
        return False


def listen():
    """
    主要的调度器，读一个IP，读一个code，执行submit操作
    :return:
    """
    while True:
        try:
            status()
            ip, code = get_ip(), get_code()
            resp = submit(code, ip)
            print("code", code, "ip", ip, "resp", resp)
            if "1000" in resp:
                used.add(ip)
                ui.success("投票成功")
        except Exception as ex:
            print(ex)


def load_ips_from(filename):
    global ips
    filepath = os.path.join(os.path.dirname(__file__), filename)
    a = re.findall("\d+\.\d+\.\d+.\d+:\d+", open(filepath, encoding='utf8').read())
    print(a)
    for i in a:
        if test_ip(i):
            ips.append(i)


def get_ip_thread():
    if mode == "crawl":
        crawl_ip()
    elif mode == "text":
        load_ips_from("ip.txt")


if __name__ == '__main__':
    Thread(target=get_ip_thread).start()
    Thread(target=listen).start()
    app.run(debug=False, port=8000)
