from django.conf.urls import url, include
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Address Book API')

from . import views

urlpatterns = [
    # url(r'^upload/$', views.upload, name='upload'),
    # url(r'^docs/', schema_view),
    url(r'^photo/$', views.PhotoList.as_view(), name='myphoto-list'),
    url(r'^photo/(?P<pk>[0-9]+)/$', views.PhotoDetail.as_view(), name='myphoto-detail'),
]
