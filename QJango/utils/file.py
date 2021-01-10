"""

"""

import os
def open_dir(path:str,select=False):
    path = path.replace('/','\\')
    if select:
        os.system('explorer.exe /select, "%s"' % path)
    else:
        os.system("explorer.exe %s" % path)
