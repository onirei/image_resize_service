from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from img_resizer import views


urlpatterns = [
    url(r'^$', views.ImageListView.as_view()),
    url(r'^page=(?P<page>\d+)/$', views.ImageListView.as_view()),
    url(r'^upload/$', views.UploadImageView.as_view()),
    url(r'^(?:(?P<img_hash>\w+)/)?$', views.ImageDetailView.as_view()),
    url(r'^delete/(?:(?P<pk>\d+)/)?$', views.DeleteImageView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
