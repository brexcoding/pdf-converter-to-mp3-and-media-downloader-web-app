from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include ,re_path
from django.contrib import admin



urlpatterns = [
    re_path("adis",admin.site.urls),
    path('' , include('pdf_handler.urls')),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 