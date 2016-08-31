from django.contrib import admin

from .models import Annotation, KindOfOffence


class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('is_hate_speech', 'kinds', 'comment')
    list_filter = ('is_hate_speech', 'kind')


admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(KindOfOffence)
