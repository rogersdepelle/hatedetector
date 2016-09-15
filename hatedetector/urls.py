from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from web_scraping.utils import dump
from annotation.views import annotation, annotation_admin, annotation_login, annotation_logout

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/annotation/')),
    url(r'^annotation/$', annotation, name='annotation'),
    url(r'^annotation/login/', annotation_login, name='annotation_login'),
    url(r'^annotation/logout/', annotation_logout, name='annotation_logout'),
    url(r'^annotation/admin/', annotation_admin, name='annotation_admin'),
    url(r'^dump/', dump, name='dump'),
    url(r'^admin/', admin.site.urls),
]

admin.site.site_header = 'Hate Detector'
admin.site.site_title = 'Hate Detector'
admin.site.index_title = ''
admin.site.site_url = '/'
