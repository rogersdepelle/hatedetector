from django.contrib import admin

from .models import *


class SystemDataAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    return not SystemData.objects.exists()


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'order')


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(SystemData, SystemDataAdmin)
