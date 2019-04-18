from django.conf.urls import url
from api_v1 import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^images/$', views.ImageList.as_view()),
    url(r'^images/(?:(?P<img_hash>\w+)/)?$', views.ImageDetail.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
























# image_list = views.ImageViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# urlpatterns = [
#     url(r'^images/$', image_list, name='post_list'),
# ]
#
#
# urlpatterns = format_suffix_patterns(urlpatterns)

# router = routers.DefaultRouter()
# router.register(r'images', views.ImageViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
#     ]

# urlpatterns = [
#     path('', include(router.urls)),
#     # url(r'^$', views.ImageViewSet.as_view()),
#     # url(r'^(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
#     # url(r'^upload/$', views.FileUploadView.as_view())
#     ]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)