from django.contrib import admin

from .models import Comment, Domain, News

admin.site.register(Comment)
admin.site.register(Domain)
admin.site.register(News)
