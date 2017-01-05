from django.conf import settings
from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin

from dashboard.models import SystemData


urlpatterns = [
    url(r'^', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    data = SystemData.objects.all()[0]
    name = data.name
except:
    name = 'Dashboard'

admin.site.site_header = name
admin.site.site_title = name
admin.site.index_title = 'Admin'

handler400 = 'dashboard.views.bad_request'
handler403 = 'dashboard.views.permission_denied'
handler404 = 'dashboard.views.page_not_found'
handler500 = 'dashboard.views.server_error'
