 
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from api.views import index
urlpatterns = [
    path('',index),
    path('admin/', admin.site.urls),
    path('',include('api.urls'))
]

#adding media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)