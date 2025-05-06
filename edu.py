import baseFunctions as bf
import cv2
import time
import numpy as np
from PIL import ImageGrab as ig
import pyautogui
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def Auto_Open():
    img_unity = cv2.imread(resource_path("edu/start.png"), cv2.IMREAD_GRAYSCALE)
    img_search = cv2.imread(resource_path("edu/search.png"), cv2.IMREAD_GRAYSCALE)
    img_text = cv2.imread(resource_path("edu/clicktext.png"), cv2.IMREAD_GRAYSCALE)

    print("Open Unity")
    start_unity = bf.findLocWithKp(img_unity)
    bf.animateMoveAnddoubleClick(bf.getCurPos(), start_unity)
    time.sleep(5)
    print("Open text")
    start_search = bf.findLocWithKp(img_search)
    bf.animateMoveAndClick(bf.getCurPos(), start_search)
    time.sleep(5)
    pyautogui.write("txt", interval=0.25)
    time.sleep(2)
    start_text = bf.findLocWithKp(img_text)
    bf.animateMoveAndClick(bf.getCurPos(), start_text)

if __name__ == '__main__':
    Auto_Open()
