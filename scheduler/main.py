import random

import requests

from random_name.random_name import random_name

# 提交表单的地址
submit_url = "http://vote.zazhipu.com/Client/WoDoVote"


def submit(code, ip):
    qq = str(random.randint(10000000, 1e9))
    data = {
        "Name": random_name(),
        "QQ": qq,
        "Email": qq + "@qq.com",
        "Code": code,
        "Id": "7b655518-2301-4801-bd3a-b47fe5bbb603"
    }
    proxies = dict(http=ip) if ip else None
    resp = requests.post(submit_url, data, proxies=proxies)
    print(resp.text)
    return resp.text
