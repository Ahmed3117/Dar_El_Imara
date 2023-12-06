
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('maindata.urls',namespace='maindata')),
    path('subdata/', include('subdata.urls',namespace='subdata')),
    path('userdata/', include('userdata.urls',namespace='userdata')),
    path('inoutpay/', include('inoutpay.urls',namespace='inoutpay')),
    path('worksdata/', include('worksdata.urls',namespace='worksdata')),
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
