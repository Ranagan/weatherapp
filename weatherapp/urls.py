"""weatherapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url

from weatherapp.core import views

urlpatterns = [
    url(r'^api/get-outside-temp/$', views.OutsideTempView.as_view()),
    url(r'^api/get-hi-temp/$', views.HiTempView.as_view()),
    url(r'^api/get-forecast/$', views.ForecastView.as_view()),
    url(r'^api/', include('rest_framework.urls')),
]

from rest_framework.urlpatterns import format_suffix_patterns
