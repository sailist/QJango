"""

"""


# from ui.main import start
# from ui.app import start
def run():
    from manage import setup

    setup()

    from QJango.urls import qt_patterns
    from QJango.tray import EJango
    from QJango.settings import QT_APPS
    from QJango.events import handler
    import importlib

    for app in QT_APPS:
        # 引入 路由
        try:
            importlib.import_module("{}.{}".format(app, "route"))
        except:
            pass

        try:
            module = importlib.import_module("{}.{}".format(app, "apps"))
            handler.default(module.default())
        except:
            pass

    app = EJango()
    for name, val in qt_patterns().items():
        window = val['entry']()
        app.regist_app(
            window=window,
            name=name,
            show_now=val.get('show_now', False),
            show_event=val.get('show_event', None),
            show_shortcut=val.get('show_shortcut', None),
            showable=val.get('showable', True)
        )

    app.start()


if __name__ == '__main__':
    run()
