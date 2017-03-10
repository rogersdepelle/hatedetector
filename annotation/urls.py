from django.conf.urls import url
from django.contrib import admin

from .views import *


urlpatterns = [
    url(r'^$', annotation, name="annotation"),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^export/$', export, name="export"),
    url(r'^arff/$', arff, name="arff"),
    url(r'^kappa/$', kappa, name="kappa"),
]
