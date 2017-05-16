from django.contrib import admin

from .models import Annotation, Annotator, KindOfOffence


class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('annotator', 'is_hate_speech','kinds', 'comment')
    list_filter = ('is_hate_speech', 'kind')


admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(KindOfOffence)
admin.site.register(Annotator)
