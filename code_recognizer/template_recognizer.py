import os

import numpy as np
from skimage import io, feature, draw

from code_recognizer.load_templates import tem_body, strip

"""
主要的验证码破解器
"""

debug = False  # __name__ == "__main__"


def get_index(img, tem):
    resp = feature.match_template(img, tem)
    ma = np.argmax(resp)
    x, y, _ = np.unravel_index(ma, resp.shape)
    print(x, y, resp[x][y])
    if resp[x][y] > 0.5:
        return x, y
    return None, None


def load_image(filename="haha-demo.png"):
    img = io.imread(os.path.join(os.path.dirname(__file__), "..", "resource", filename))
    img = img[:, :, :3]
    return img


def recognize():
    img = load_image()
    img, xx, yy = strip(img)
    main_img = img[55:209, :, :]
    word_img = img[220:290, 93:250, :]
    ans = [(0, 0)] * len(tem_body)
    for index, i in enumerate(tem_body[:3]):
        x, y = get_index(word_img, i)
        if not x: continue
        ans[index] = get_index(img, word_img[x:x + 50, y:y + 50, :])
        if debug:
            word_img[x:x + 10, y:y + 10, :] = (255, 0, 0)
            io.imshow(word_img)
            io.show()
    for index, i in enumerate(tem_body[3:]):
        x, y = get_index(main_img, i)
        if not x: continue
        # 转换坐标为全局坐标
        print(index)
        ans[index + 3] = get_index(img, main_img[x:x + 50, y:y + 50, :])
        if debug:
            main_img[x:x + 10, y:y + 10, :] = (255, 0, 0)
            io.imshow(main_img)
            io.show()
    ans = sort_by_location(ans)
    for i in range(len(ans)):
        ans[i] = np.array(ans[i]) + (xx, yy)
    return ans


def sort_by_location(a):
    for i in range(3):
        for j in range(i, 3):
            if tuple(a[i]) < tuple(a[j]):
                a[i], a[j] = a[j], a[i]
                a[i + 3], a[j + 3] = a[j + 3], a[i + 3]
    ans = []
    for x, y in a[3:]:
        if x and y:
            ans.append((x, y))
    return ans


def visualize(ans):
    img = load_image()
    for x, y in ans:
        if x == 0 and y == 0: continue
        paint_index = draw.circle(x, y, 5)
        img[paint_index] = (255, 0, 0)
    return img


if __name__ == '__main__':
    ans = recognize()
    print(ans)
    img = visualize(ans)
    io.imshow(img)
    io.show()
