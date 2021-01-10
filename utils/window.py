import ctypes
import os
import win32gui
import win32api
from win32con import SWP_NOMOVE
from win32con import SWP_NOSIZE
from win32con import *
from win32con import SW_SHOW
from win32con import HWND_TOPMOST
from win32con import GWL_EXSTYLE
from win32con import WS_EX_TOOLWINDOW


def find_window(name):
    return win32gui.FindWindow(None, name)


def open_window(path):
    os.popen(path)


def hide_from_taskbar(hw):
    win32gui.ShowWindow(hw, SW_MINIMIZE)
    return win32gui.ShowWindow(hw, SW_HIDE)


def set_topmost(hw):
    win32gui.ShowWindow(hw, SW_SHOWDEFAULT)
    win32gui.ShowWindow(hw, SW_SHOW)
    # win32gui.SetActiveWindow(hw)
    # win32gui.BringWindowToTop(hw)
    win32gui.SetForegroundWindow(hw)


def has_focus(hw):
    return GetForegroundWindow() == hw


GetForegroundWindow = win32gui.GetForegroundWindow
