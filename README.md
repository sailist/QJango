# QJango
Qt with Django database and extra UI components

Qt 开发工具包，以Django的应用架构为基础，添加了一个事件处理系统。

仅在 Win10 上运行成功过，所有特性不一定均支持 Mac，Linux。

## Features
 - 可以使用 Django 的数据库快速开发
 - 复写了 View 类，UI 变量定义即添加
 
# How to use

```
git clone https://github.com/sailist/QJango
git clone https://github.com/sailist/QJango <Your app name>
```

## create app
````
python manage.py startapp <appname>
python manage.py startapp recite
````

所有的应用在 `QJango.settings.QT_APPS` 中注册并在 urls 中添加窗体入口。


在`view.py`中写一个新窗体作为入口：
```python
from PyQt5.QtWidgets import *

class XXXWindow(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.shortcut_open = QShortcut(QKeySequence('Esc'), self)
        # self.shortcut_open.activated.connect(lambda: self.hide())
        self.setWindowTitle('XXX')
```

在`Saiqts.urls`中注册应用入口和快捷键

```python
def qt_patterns():
    from <app>.views import <Widget>
    from <app>.apps import Event as PEvent
    return {
        '<app>': {
            "showable": False, # 是否可唤出（后台应用不需要有界面）
            "show_now": False, # 应用启动时唤出（默认为 False）
            "entry": <Widget>, # 应用入口
            "show_shortcut": 'Shift+Ctrl+A', # 唤出快捷键（全局），（可选）
            "show_event": PEvent.hide_to_show, # 唤出时是否调用某事件（可选）
        },
    }
```


## 



## 快捷键
定义在 `component.utils` 中，基于 Qt 内的 `QShortcut`（应用内快捷键） 和`pyqtkeybind`（全局快捷键） 
```
def AddShortCut(widget, keyseq: str, func, global_shortcut=False)
```


```python
from components.utils import AddShortCut
function = lambda : print('hello shortcut')
AddShortCut(..., 'Ctrl+Shift+Y', function)
AddShortCut(..., 'Ctrl+Shift+Alt+Y', function, global_shortcut=True)
```

## 事件、状态系统

该部份参考了 `vue`

在每个应用的`app.py` 中添加 `Event`, `State`, `Constant`


```python

class Event:
    """事件"""
    someting_happen = 'happen_name'


class State:
    """可变全局变量"""
    search_text = 'filter_text'


class Constant:
    """常量"""

    class FILTER_FLAG:
        tag = 'tag'

    class FILTER_DESC:
        tag = 'Filter by Tags'
```


### 事件
注册
```python
from .apps import Event 
from QJango.events import *
function = lambda *args: print('hello world', args)
handler.on(Event.someting_happen, function)
```

发送
```python
from .apps import Event
from QJango.events import *
handler.emit(Event.someting_happen, 1,2,3,4)
```

### 状态
提交，更改某状态的值
```python
from .apps import State
from QJango.events import *
handler.commit(State.search_text, "search_text")
```

获取某状态的值
```python
from .apps import State
from QJango.events import *
print(handler.state(State.search_text))
```

### 延迟事件
该部份含义参考 rx 系列代码示意（如 rxjava）

```python
from .apps import Event, State
from QJango.events import timer

timer.io()
timer.consume()
timer.debounce()
timer.throttle()
```

### 应用间联动
事件是统一在全局注册的，因此事件可以在应用间相互传递，引入不同应用即可。

```python
from <app>.apps import *
```

## Win10 通知

```python
from QJango.events import *
targs = dict(title="title", msg="message", duration=2, threaded=True)
handler.emit(GEvents.on_make_toast, 0, (), targs)
```


## 其他应用联动



## web 后端
该部份基于 flask，额外开了一个线程部署后端

在每个应用的 `route.py` 中声明 `api`，应用会自动搜集

```python
from flask import request,jsonify

from QJango.route import app


@app.route('/api/manic/what',methods=['GET','POST'])
def get_test():
    print(request.headers)
    print(request.args)
    print(request.data)
    return jsonify()
```


下载文件
```python
import os

from flask import send_from_directory

from QJango import settings
from QJango.route import app


@app.route('/api/download/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    """
    :param filename:{tid}/...
    :return:
    """
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)

    fn = os.path.join(settings.MEDIA_ROOT, 'pdf', filename)
    path, fname = os.path.split(fn)
    from .apps import Event
    from QJango.events import handler
    handler.emit(Event.on_download_paper)
    return send_from_directory(path, fname, as_attachment=True)
```


## 外部应用唤醒
一些启动较慢的应用，可以通过这种方式折中，定义一个全局快捷键进行切换。

```python
from utils import window
path = ".../xxx.exe"

hw = window.find_window("xxx")
if hw == 0:
    window.open_window(path)

hw = window.find_window("xxx")
window.hide_from_taskbar(hw) # 隐藏（可以视作关闭）
window.set_topmost(hw) # 唤醒
window.has_focus(hw) # 是否有焦点
```

