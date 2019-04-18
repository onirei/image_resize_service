from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from img_resizer import views


urlpatterns = [
    url(r'^$', views.show_image_list),
    url(r'^upload/$', views.download_image),
    url(r'^(?:(?P<img_hash>\w+)/)?$', views.show_image),
    url(r'^delete/(?:(?P<pk>\d+)/)?$', views.del_image),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
