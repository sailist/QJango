"""

"""

from collections import OrderedDict

from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from pyqtkeybind import keybinder

__init = False


class __WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0



def AddShortCut(widget, keyseq: str, func, global_shortcut=False):
    """

    :param widget:
    :param keyseq:
    :param func:
    :param global_shortcut: 是否全局快捷键
    :return:
    """
    if global_shortcut:
        global __init,__event_dispatcher,__win_event_filter
        if not __init:
            keybinder.init()
            __event_dispatcher = QAbstractEventDispatcher.instance()
            __win_event_filter = __WinEventFilter(keybinder)
            __event_dispatcher.installNativeEventFilter(__win_event_filter)
            keybinder.register_hotkey(widget.winId(), keyseq, func)
            __init = True
        else:
            keybinder.register_hotkey(widget.winId(), keyseq, func)
    else:
        short_cuts = getattr(widget, '_short_cuts', OrderedDict())
        shortcut = QShortcut(QKeySequence(keyseq), widget)
        shortcut.activated.connect(func)
        short_cuts[keyseq] = shortcut
        widget._short_cuts = short_cuts
    return widget
