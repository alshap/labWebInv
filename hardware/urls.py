from django.conf.urls import url

from . import views

app_name = 'hardware'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>[0-9]+)/$', views.DevicesView.as_view(), name='devices'),
        url(r'^(?P<category_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.HardwareRequestView.as_view(), name='hardware_request'),
        url(r'^(?P<hardware_id>[0-9]+)/take/$', views.take, name='take'),
        url(r'^view/([0-9]+)/$', views.set_obj_view, name='setview'),
    ]