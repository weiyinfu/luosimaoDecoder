from matplotlib import pyplot as plt
from matplotlib.widgets import Button, RadioButtons
from PIL import Image
from skimage import data
from code_recognizer.template_recognizer import load_image, get_index, strip

"""
人工识别验证码
"""
a = []

def on_press(event):
    if event.inaxes is None:
        print("none")
        return
    print(event)
    a.append((event.xdata, event.ydata))
    ax = event.inaxes
    ax.scatter(event.xdata, event.ydata)


def recognize():
    a.clear()
    original_img = load_image("haha.png")
    img, xx, yy = strip(original_img)
    fig = plt.figure()
    fig.canvas.mpl_connect("button_press_event", on_press)
    ax1 = fig.add_subplot(111)
    ax1.imshow(img)
    plt.axis("off")
    plt.show()
    original = load_image()
    for i in range(len(a)):
        x, y = a[i]
        x, y = int(x + xx), int(y + yy)
        a[i] = (x, y)
        original[x:x + 10, y:y + 10, :] = (255, 0, 0)
    return a


if __name__ == "__main__":
    recognize()
