"""

"""

import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractEventDispatcher, QAbstractNativeEventFilter
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from pyqtkeybind import keybinder
from win10toast import ToastNotifier
from components.mixin.HideClose import WrapHideClose
from .events import handler, GEvents, timer


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class EJango:
    def __init__(self):
        sys.excepthook = self.excepthook
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.icon = QIcon("./src/favicon.ico")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.tray.messageClicked.connect(lambda *args: print(args))

        self.menu = QMenu()
        self._actions = []
        quit = QAction("Quit")
        quit.triggered.connect(self.app.quit)
        self._actions.append(quit)
        # self.menu.addAction(quit)
        self.tray.setContextMenu(self.menu)

        keybinder.init()
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)

        handler.on(GEvents.on_make_toast, self.on_make_toast)

    def start(self):
        from .route import run
        from .events import timer
        self.menu.addActions(reversed(self._actions))
        timer.io(lambda: run())
        ret = self.app.exec_()
        sys.exit(ret)

    def excepthook(self, exc_type, exc_value, exc_tb):
        import traceback
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        with open('./logs/err.log', 'a', encoding='utf-8') as w:
            w.write(tb)
        traceback.print_tb(tb)
        QApplication.quit()

    def on_make_toast(self, args, targs, kwargs):
        print(targs, kwargs)
        ToastNotifier().show_toast(*targs, **kwargs)

    def regist_app(self, window: QMainWindow, name: str, show_now: bool = True, show_shortcut: str = None,
                   show_event: str = None, showable=True):
        def show_wrap():
            if show_event is not None:
                handler.emit(show_event)

            if not showable:
                return
            window.show()
            window.activateWindow()
            window.setWindowState(QtCore.Qt.WindowActive)

        WrapHideClose(window)

        self.shortcut_open = QShortcut(QKeySequence('Esc'), window)
        self.shortcut_open.activated.connect(lambda: window.hide())

        show_trig = QAction(name)
        show_trig.triggered.connect(show_wrap)
        self._actions.append(show_trig)
        # self.menu.addAction(show_trig)

        if show_shortcut is not None:
            keybinder.register_hotkey(window.winId(), show_shortcut, show_wrap)
