from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from img_resizer import views


urlpatterns = [
    url(r'^$', views.show_image_list, name='create_task'),
    url(r'^upload/$', views.download_image, name='task_list'),
    url(r'^<image_hash>/?query_params/$', views.show_image, name='task_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)