from django.conf.urls import url

from . import views

app_name = 'hardware'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>[0-9]+)/$', views.DevicesView.as_view(), name='devices'),
        url(r'^(?P<category_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.HardwareRequestView.as_view(), name='hardware_request'),
        url(r'^(?P<hardware_id>[0-9]+)/take/$', views.take, name='take'),
        url(r'^view/([0-9]+)/$', views.set_obj_view, name='setview'),
        url(r'^search/$', views.hardware_search, name='hardware_search'),
    ]
"""
Contains hardware app all urls.

names:

* index => main app page. Template displays categories set.
* devices => certain category page. Template displays hardware set based on category.
* hardware_request => Hardware request form template.
* take => Function on success hardware_request form post.
* setview => Sets the card or list view to the index and devices views.
* hardware_search => Function on success search form.
"""