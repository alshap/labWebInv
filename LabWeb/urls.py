"""LabWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import change_language
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
        path('change_language/',change_language,name='change_language')
    ]
urlpatterns += i18n_patterns(
        url(_(r'^admin/'), admin.site.urls),
        url(_(r'^hardware/'), include('hardware.urls')),
        url(_(r'^explore_online/'), include('explore_online.urls')),
        url(_(r'^projects/'), include('projects.urls')),
        url(_(r'^guides/'), include('guides.urls')),
        path('', include('home.urls')),
        prefix_default_language = False
    )
urlpatterns += staticfiles_urlpatterns()
