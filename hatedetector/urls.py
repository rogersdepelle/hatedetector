from django.conf.urls import url
from django.contrib import admin

from web_scraping.utils import dump

urlpatterns = [
    url(r'^dump/', dump, name='dump'),
    url(r'^', admin.site.urls),
]

admin.site.site_header = 'Hate Detector'
admin.site.site_title = 'Hate Detector'
admin.site.index_title = 'Annotation Data'
admin.site.site_url = '/dump/'
