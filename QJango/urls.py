"""QJango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


def qt_patterns():
    # from <app>.views import <window>
    # from <app>.apps import Event
    return {
        '<app>': {
            # "entry": <window>,
            # # "show_shortcut": 'Shift+Ctrl+A',
            # "show_event": Event.hide_to_show,
            # "show_now": False,
            # "showable": False,
        },
    }
