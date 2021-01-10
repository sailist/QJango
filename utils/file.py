"""

"""

import os

from QJango import settings


def open_file(file):
    ext = os.path.splitext(file)[1]
    cmd = settings.VIEWER.get(ext, None)
    if cmd is None:
        os.popen(file)
    else:
        os.popen(cmd.format(file=file))
