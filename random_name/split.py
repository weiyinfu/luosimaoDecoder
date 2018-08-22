a = open("haha.txt", encoding='utf8').read().split()
b = open("百家姓.txt", encoding='utf8').read()
import re

b = re.sub("[^\u4e00-\u9fa5]", "", b)
s = ""
i = 0
while i < len(b):
    if b[i:i + 2] in a:
        s += b[i:i + 2]
        i += 2
    elif b[i] in a:
        s += b[i]
        i += 1
    else:
        i += 1
    s += " "
import sys

sys.stdout = open("splited百家姓.txt", "w", encoding='utf8')
print(s)
