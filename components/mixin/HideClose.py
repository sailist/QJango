"""

"""
from PyQt5.QtWidgets import QWidget, QMainWindow
from typing import Union

def WrapHideClose(widget:Union[QWidget,QMainWindow]):
    def wrap(event):
        widget.setVisible(False)
        event.ignore()

    widget.closeEvent = wrap
    return widget

