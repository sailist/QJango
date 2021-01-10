"""

"""
from typing import Callable,Any

from PyQt5 import QtCore
from PyQt5.QtWidgets import QItemDelegate, QLineEdit


class EditDelegate(QItemDelegate):

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: 'QStyleOptionViewItem',
                    index: QtCore.QModelIndex) -> bool:
        # res = super().editorEvent(event, model, option, index)
        if event.type() in {6, 2}:  # 6 是 F2, 2 是单击，分别相应编辑和选中状态
            return False

        # 其他情况 （3,4 ，具体对应鼠标的两个事件） 返回True，这里是用于屏蔽双击事件的编辑状态
        return True

    def registSetModelDataEvent(self, func: Callable[[QLineEdit, Any, QtCore.QModelIndex], None]):
        self._func = func
        # lst.append(func)
        # self.lst = lst

    def setModelData(self, editor: QLineEdit, model, index):
        func = getattr(self,'_func',None)
        if func is not None:
            func(editor, model, index)
