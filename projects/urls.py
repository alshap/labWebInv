from django.conf.urls import url

from . import views

app_name = 'projects'
urlpatterns = [
         url(r'^$', views.IndexView.as_view(), name='index'),
         url(r'^data_saver/$', views.data_saver, name='data_saver'),
         url(r'^(?P<project_id>[0-9]+)/$', views.getinfo, name='getinfo'),
    ]