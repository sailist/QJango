"""

"""
from collections import OrderedDict
from typing import Any, Union

from PyQt5.QtWidgets import *

__all__ = ['EAddWrap', "EAddMixin"]


class EAddMixin():
    """
    some.xx =
    """

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name.startswith("_"):
            return
        if isinstance(self, QMainWindow):
            if isinstance(value, QBoxLayout):
                EAddWrap(value)
                widget = QWidget()
                widget.setLayout(value)
                self.setCentralWidget(widget)
            elif isinstance(value, QWidget):
                EAddWrap(value)
                self.setCentralWidget(value)
        elif isinstance(self, QWidget):
            if isinstance(value, QBoxLayout):
                EAddWrap(value)
                self.setLayout(value)
            # elif isinstance(value,QWidget):
            #     self.addW
        elif isinstance(self, QBoxLayout):
            if isinstance(value, QBoxLayout):
                EAddWrap(value)
                layout_dict = getattr(self, 'layout_dict', OrderedDict())
                layout_dict[name] = value
                self.layout_dict = layout_dict
                self.addLayout(value)
            elif isinstance(value, QWidget):
                EAddWrap(value)
                widget_dict = getattr(self, 'widget_dict', OrderedDict())
                widget_dict[name] = value
                self.widget_dict = widget_dict
                self.addWidget(value)


def EAddWrap(self: Union[QBoxLayout, QWidget]):
    _setattr = self.__class__.__setattr__

    def wrap(self, name: str, value: Any):
        _setattr(self, name, value)
        if name.startswith("_"):
            return
        if isinstance(self, QWidget):
            if isinstance(value, QBoxLayout):
                EAddWrap(value)
                layout_dict = getattr(self, 'layout_dict', OrderedDict())
                layout_dict[name] = value
                self.layout_dict = layout_dict
                self.setLayout(value)
        elif isinstance(self, QBoxLayout):
            if isinstance(value, QBoxLayout):
                EAddWrap(value)
                layout_dict = getattr(self, 'layout_dict', OrderedDict())
                layout_dict[name] = value
                self.layout_dict = layout_dict
                self.addLayout(value)
            elif isinstance(value, QWidget):
                EAddWrap(value)
                widget_dict = getattr(self, 'widget_dict', OrderedDict())
                widget_dict[name] = value
                self.widget_dict = widget_dict
                self.addWidget(value)

    self.__class__.__setattr__ = wrap
    return self
