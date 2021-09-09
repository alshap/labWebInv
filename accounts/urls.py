from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        
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