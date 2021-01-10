"""

"""

import time
from collections import defaultdict
from typing import Callable

from PyQt5.QtCore import *

__all__ = ['handler', 'timer', 'condition', 'Condition']


class EventHandler:
    def __init__(self) -> None:
        self.listener = dict()
        self.checks = defaultdict(list)
        self.emitter = dict()
        self._mutations = {}

    def default(self, val: dict):
        self._mutations.update(val)

    def on(self, name, func, *checks):
        """注册某事件的监听器"""
        if name not in self.listener:
            def __(arg):
                name, args, kwargs = arg
                print(arg)
                for func in self.listener[name]:
                    if len(checks) == 0 or all([check() for check in checks]):
                        func(*args, **kwargs)

            self.listener[name] = []
            sig = Sig()
            sig.fine.connect(__)
            self.emitter[name] = sig

        self.listener[name].append(func)

    def emit(self, name, *args, **kwargs):
        """发生某事件"""
        # for func in self.listener[name]:
        #     func(name, *args, **kwargs)
        if name in self.emitter:
            self.emitter[name].fine.emit((name, args, kwargs))

    def commit(self, name, value, event=None):
        """注册获取某state 值的方法"""
        # print(name, 'to', value)
        self._mutations[name] = value
        if event is not None:
            self.emit(event)

    def state(self, name):
        """返回某 state 的值"""

        return self._mutations.get(name, None)

    def __getattr__(self, item):
        def foo(*args, **kwargs):
            self.emit(item, *args, **kwargs)

        return foo

    def __getitem__(self, item):
        def foo(*args, **kwargs):
            self.emit(item, *args, **kwargs)

        return foo


class Sig(QObject):
    fine = pyqtSignal(tuple)


class LazyWork(QThread):
    fine = pyqtSignal(object)

    def __init__(self, time: int, func: Callable, exec=False):
        QThread.__init__(self, )
        self.time = time
        self.func = func
        self.exec__ = exec
        self.disposed = False

    def run(self):
        start = time.time()
        print(self.time)
        while time.time() - start < self.time:
            time.sleep(1)

        if self.disposed:
            return
        try:
            if self.exec__:
                self.func()
            else:
                self.fine.emit(self.func)
        except Exception as e:
            pass

        self.disposed = True


class TimerEvent():
    def __init__(self):
        self.event_dict = dict()
        self.thread_pool = QThreadPool()

    def _add_time_event(self, name: str, func: Callable, time: int):
        val = LazyWork(time, func)

        def __(f):
            f()

        val.fine.connect(__)

        val.start()
        self.event_dict[name] = val

    def consume(self, func: Callable, time: int = 0):
        self._add_time_event('__', func, time)
        # val = LazyWork(time, func)
        # val.start()

    def io(self, func: Callable):
        val = LazyWork(time=0, func=func, exec=True)
        val.start(QThread.IdlePriority)
        self.event_dict["__"] = val
        # self.event_dict[name] = val

    def debounce(self, name: str, func: Callable, time: int = 0):
        """节流，一定时间内多次点击只运行最后一次"""
        val = self.event_dict.get(name, None)  # type:LazyWork
        if val is not None and not val.disposed:
            val.terminate()

        self._add_time_event(name, func, time)

    def throttle(self, name: str, func: Callable, time: int = 0):
        """防抖，一定时间内只运行一次"""
        val = self.event_dict.get(name, None)  # type:LazyWork
        if val is None or val.disposed:
            self._add_time_event(name, func, time)


def condition(*judges: Callable):
    def wrap(func):
        def inner(*args, **kwargs):
            if all([judge() for judge in judges]):
                return func(*args, **kwargs)
            else:
                return None

        return inner

    return wrap


class Condition:
    @staticmethod
    def check():
        return True

    def __new__(cls, func):  # real signature unknown
        def wrap(*iargs, **ikwargs):
            if cls.check():
                func(*iargs, **ikwargs)

        return wrap


class GEvents():
    on_make_toast = 'on_make_toast'


timer = TimerEvent()

handler = EventHandler()
