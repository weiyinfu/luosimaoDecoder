import numpy as np
from matplotlib import pyplot as plt
from skimage import io
import os

"""
加载模板
"""
tem = io.imread(os.path.join(os.path.dirname(__file__), "../resource/templates.bmp"))

tem_body = []


def load_tems():
    # 加载字符
    CHAR_SIZE = 30
    i = 0
    while i < tem.shape[0]:
        j = 0
        while j < tem.shape[1] and i < tem.shape[0]:
            if tuple(tem[i][j]) != (255, 255, 255):
                tem_body.append(
                    tem[max(i - CHAR_SIZE // 4, 0):min(i + CHAR_SIZE, tem.shape[0]),
                    max(j - CHAR_SIZE // 4, 0):min(j + CHAR_SIZE, tem.shape[1])])
                i += 30
                j += 30
            else:
                j += 1
        i += 1


def strip(body):
    max_x = body.shape[0] - 1
    min_x = 0
    max_y = body.shape[1] - 1
    min_y = 0
    while not np.any(np.subtract(body[max_x, :].reshape(-1), 255)):
        max_x -= 1
    while not np.any(np.subtract(body[:, max_y].reshape(-1), 255)):
        max_y -= 1
    while not np.any(np.subtract(body[min_x, :].reshape(-1), 255)):
        min_x += 1
    while not np.any(np.subtract(body[min_y, :].reshape(-1), 255)):
        min_y += 1
    return body[min_x:max_x, min_y:max_y], min_x, min_y


def better(body, want):
    # 只显示字符的黑色部分
    body, _, _ = strip(body)
    max_y = 0
    min_y = body.shape[1]
    max_x = 0
    min_x = body.shape[0]
    not_want = np.array([255, 255, 255]) - want
    for i in range(body.shape[0]):
        for j in range(body.shape[1]):
            if np.linalg.norm(body[i][j] - want) < 100:
                min_y = min(min_y, j)
                max_y = max(max_y, j)
                min_x = min(min_x, i)
                max_x = max(max_x, i)
                body[i][j] = want
            else:
                body[i][j] = not_want
    return body[min_x:max_x, min_y:max_y]


load_tems()
for index, body in enumerate(tem_body):
    tem_body[index] = better(body, [0, 0, 0] if index < 3 else [255, 255, 255])

if __name__ == '__main__':
    for i in tem_body:
        print(i.shape)
        io.imshow(i)
        plt.show()
