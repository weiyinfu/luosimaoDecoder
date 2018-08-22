import time
from threading import Thread

from flask import Flask, request, make_response
import requests
from pyquery import PyQuery as pq
from scheduler.main import submit

app = Flask(__name__)

codes = []
ips = []
used = set()  # 已经用过的IP


@app.route("/code/")
def code():
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
    print("ips", len(ips), "codes", len(codes))


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
        if len(ips) < 100:
            status()
            urls = ["http://www.xicidaili.com/nn",
                    "http://www.xicidaili.com/nt",
                    "http://www.xicidaili.com/wn",
                    "http://www.xicidaili.com/wt"]
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
                })
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


def test_ip(ip):
    """
    测试IP可用性
    :param ip:
    :return:
    """
    print("testing ip", ip)
    try:
        if ip in used:
            return False
        resp = requests.get("http://www.baidu.com", proxies=dict(http="http://" + ip), timeout=5)
        print("test result", resp.status_code)
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
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    Thread(target=crawl_ip).start()
    Thread(target=listen).start()
    app.run(debug=False, port=8000)
