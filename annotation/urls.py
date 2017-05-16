from django.conf.urls import url
from django.contrib import admin

from .views import *


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^annotation/$', annotation, name="annotation"),
    url(r'^start/$', start, name="start"),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^congratulations/$', congrat, name="congrat"),
    url(r'^arff/$', arff, name="arff"),
]
