import pyautogui
from pyscreeze import ImageNotFoundException
import os
import time

WIDTH, HEIGHT = pyautogui.size()


def image_click(file, duration=0.1, xoffset=0, yoffset=0, confidence=0.7, region=(0, 0, WIDTH, HEIGHT)):
    x, y, w, h = find_image_screenshot(file, confidence=confidence, region=region)
    pyautogui.moveTo(x + w / 2 + xoffset, y + h / 2 + yoffset, duration=duration)
    pyautogui.mouseDown(pyautogui.position())
    time.sleep(0.1)
    pyautogui.mouseUp(pyautogui.position())
    time.sleep(0.1)
    return True


def move_click(x, y, duration=0.1):
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.mouseDown(pyautogui.position())
    time.sleep(0.1)
    pyautogui.mouseUp(pyautogui.position())
    time.sleep(0.1)


def find_image_screenshot(file, exit_on_not_found=True, confidence=0.7, region=(0, 0, WIDTH, HEIGHT)):
    if not os.path.exists(os.path.join('temp')):
        os.mkdir('temp')
    pyautogui.screenshot(os.path.join('temp', 'tempScreenshot.png'))
    try:
        box = pyautogui.locate(
            file,
            os.path.join('temp', 'tempScreenshot.png'),
        )
        os.remove(os.path.join('temp', 'tempScreenshot.png'))

        if box is not None:
            return box.left, box.top, box.width, box.height
        else:
            if exit_on_not_found:
                return exit('could not find ' + file)
            else:
                return False
    except ImageNotFoundException:
        print("could not find " + str(file) + ' on screen')
        return False
