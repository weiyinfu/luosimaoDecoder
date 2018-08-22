# 加载模板
from matplotlib import pyplot as plt
from skimage import io

tem = io.imread("templates.bmp")
tem_strs = "星形 圆点 方块".split()
tem_str_body = []
tem_shape_body = []

io.imshow(tem)
io.show()


def load_characters():
    # 加载字符
    i = 0
    while i < tem.shape[0]:
        j = 0
        while j < tem.shape[1]:
            if tuple(tem[i][j]) != (255, 255, 255):
                tem_str_body.append(tem[i:min(i + 30, tem.shape[0])][j:])
                i = min(i + 30, tem.shape[0]) - 1
                j += 30
            else:
                j += 1
        i += 1


def load_images():
    # 加载图片
    i = 0
    while i < tem.shape[0]:
        j = 0
        while j < tem.shape[1]:
            if tuple(tem[i][j]) != (255, 255, 255):
                tem_shape_body.append(tem[i:min(i + 50, tem.shape[0])][j:])
                i = min(i + 50, tem.shape[0]) - 1
                j += 50
            else:
                j += 1
        i += 1


def better_character(shape):
    # 只显示字符的黑色部分
    return shape


def better_shape(shape):
    # 只显示形状的白色部分
    return shape


load_characters()
load_images()
tem_str_body = list(map(better_character, tem_str_body))
tem_shape_body = list(map(better_shape, tem_shape_body))
print("over")
print(len(tem_str_body))
print(len(tem_shape_body))
for i in tem_shape_body + tem_str_body:
    io.imshow(i)
    plt.show()
