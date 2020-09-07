"""trackship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path, register_converter
from django.views.generic import TemplateView

from fairing.views import api_ship_list, api_ship_position_list


class SevenDigitConverter:
    regex = '[0-9]{7}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)


register_converter(SevenDigitConverter, 'imo')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('ships/', api_ship_list, name='api-fairing-ship-list'),
        path('positions/<imo>/', api_ship_position_list, name='api-fairing-ship-position-list'),
    ])),
    path('', TemplateView.as_view(template_name='fairing/index.html'), name='index'),
]
