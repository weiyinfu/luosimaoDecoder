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
    resp = requests.post(submit_url, data, proxies=proxies, timeout=4)
    print(resp.text)
    if "1006" in resp.text:
        print("验证码错误")
    elif "1000" in resp.text:
        print("投票成功")
    elif "1003" in resp.text:
        print("今日已投票")
    elif "1004" in resp.text:
        print("今日投票已结束")
    return resp.text


if __name__ == '__main__':
    code = """
    
    
    
    2JVOnly4hgdqe-eLIb54vJeLTgjs80CeSoGPOLTxXky29tPIUo0KMxC60ly6xrHCLkOS9cJIUNzG2VhIEY1UxExDe1KP0pc6dA4YEYdHrYX95mLHLEPJBfaK5TdlbKZE27j37FYpG6eUHeBaxr61gCuY872GX2UnhdY5qO3G4NrAwyDocfSvneGXSmjym4QfdzNBq7ChrIDheP4GbVXOzO31u26GyoXPOcnkSE1HUnWntkA4ppzSDXRp7CG5bO7Iz2XsB5O3Sz90NVZxayXl26rY_BTwNOQhcARArt_2PJgjqxHG83VTgA
    
    
               """.strip()

    import re
    submit(code, "45.77.134.25:8118")
