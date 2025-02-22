from django.urls import path , include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/core/', include('core.urls')),
    path('api/v1/support/', include('support.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/v1/project/', include('task_management.urls')),
    path('api/v1/like/', include('likes.urls')),
    path('health/', include('health_check.urls')),
]
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
