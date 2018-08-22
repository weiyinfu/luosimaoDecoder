import os
import random
import re


def getfile(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, encoding='utf8').read()


a = list(set(getfile("splited百家姓.txt").split()))
name = list(set(re.sub("[^\u4e00-\u9fa5]", "", getfile("滕王阁序.txt"))))


def random_name():
    return random.choice(a) + random.choice(name) + ("" if random.randint(0, 3) == 1 else random.choice(name))


if __name__ == '__main__':
    for i in range(10000):
        now = random_name()
        if now[0]=="苏":
            print(now)
