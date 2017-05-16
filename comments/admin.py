from django.contrib import admin

from .models import Comment, News

from django.db.models import Transform
from django.db.models import TextField


class TextLengthListFilter(admin.SimpleListFilter):
    title = 'Text Length'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return (
            ('1', 'de 01 a 50'),
            ('2', 'de 50 a 100'),
            ('3', '100 ou mais'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(text__iregex=r'^.{0,50}$')
        if self.value() == '2':
            return queryset.filter(text__iregex=r'^.{50,100}$')
        if self.value() == '3':
            return queryset.filter(text__iregex=r'^.{100,}$')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ([TextLengthListFilter, 'news__site'])
    list_display = (['text', 'news'])


admin.site.register(News)
admin.site.register(Comment, CommentAdmin)