"""

"""
from collections.abc import Iterable

from PyQt5 import QtGui

__all__ = ["EAddKeyPressListener", "EKeyPressWrap", "EKeyPressMixin"]


class EKeyPressMixin():
    """添加键盘监听器支持"""

    def __init__(self) -> None:
        self._key_bind = list()
        _old_key_press = getattr(self, 'keyPressEvent', None)
        if _old_key_press is not None:
            self._old_keypress = _old_key_press
            self.keyPressEvent = self._KeyPressWrap

    def _KeyPressWrap(self, keyevent: QtGui.QKeyEvent):
        for func, matchs in self._key_bind:
            if len(matchs) == 0:
                func(keyevent)
            elif keyevent.key() in matchs:
                func(keyevent)

        self._old_keypress(keyevent)

    def AddKeyPressListener(self, func, key_match=None):
        if key_match is None:
            key_match = []
        elif isinstance(key_match, Iterable):
            pass
        elif isinstance(key_match, int):
            key_match = [key_match]
        else:
            assert False
        self._key_bind.append([func, key_match])


def EKeyPressWrap(value):
    """添加键盘监听器支持"""
    mixin = EKeyPressMixin()
    _old_key_press = getattr(value, 'keyPressEvent', None)
    if _old_key_press is not None:
        mixin._old_keypress = _old_key_press
        value.keyPressEvent = mixin._KeyPressWrap
        value.AddKeyPressListener = mixin.AddKeyPressListener
    return value


def EAddKeyPressListener(value, func, keys=None):
    """
    会确保调用了 EKeyPressWrap ，如果不能添加键盘监听，那么就返回False，否则返回True
    :param value:
    :param func:
    :return:
    """
    regist_func = getattr(value, 'AddKeyPressListener', None)
    if regist_func is None:
        EKeyPressWrap(value)
    regist_func = getattr(value, 'AddKeyPressListener', None)
    if regist_func is None:
        return False

    regist_func(func, keys)

    return True
