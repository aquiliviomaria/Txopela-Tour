from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from turismo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('turismo.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
