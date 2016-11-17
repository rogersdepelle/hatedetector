from django.conf.urls import url
from django.contrib import admin

from .views import *


urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^papers/$', papers, name="papers"),
    url(r'^hatespeech/$', hatespeech, name="hatespeech"),
    url(r'^news/$', news, name="news"),
    url(r'^contact/$', contact, name="contact"),
]
