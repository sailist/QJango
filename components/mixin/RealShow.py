"""

"""

from PyQt5 import QtCore


class ERealShowMixin():
    def real_show(self):
        self.show()
        self.activateWindow()
        self.setWindowState(QtCore.Qt.WindowActive)
