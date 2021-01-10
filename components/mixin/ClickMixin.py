"""

"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel
from typing import Callable
class ELabel(QLabel):

    def addClickListener(self,func:Callable[[QtGui.QMouseEvent],None]):
        funcs = getattr(self,'click_listeners',[])
        funcs.append(func)
        self.click_listeners = funcs

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(ev)
        for func in getattr(self,'click_listeners',[]):
            func(ev)
