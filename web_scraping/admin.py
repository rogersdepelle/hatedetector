from django.contrib import admin

from .models import Comment, Domain, News

from django.db.models import Transform
from django.db.models import TextField


class TextLengthListFilter(admin.SimpleListFilter):
    title = 'Text Length'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return (
            ('1', 'De 01 a 50'),
            ('2', 'De 51 a 100'),
            ('3', '101 ou Mais'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(text__iregex=r'^.{0,50}$')
        if self.value() == '2':
            return queryset.filter(text__iregex=r'^.{50,100}$')
        if self.value() == '3':
            return queryset.filter(text__iregex=r'^.{100,}$')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('news__domain','valid', TextLengthListFilter)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Domain)
admin.site.register(News)
