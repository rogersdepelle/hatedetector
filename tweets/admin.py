from django.contrib import admin

from .models import Tweet


class TweetAdmin(admin.ModelAdmin):
    list_display = ('lang', 'text')
    list_filter = ['lang']


admin.site.register(Tweet, TweetAdmin)
