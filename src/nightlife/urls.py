"""
URL configuration for nightlife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from artists.views import spotify_callback
from events import views
from events.views import Home, Search

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('events/', include('events.urls')),
    path('artists/', include('artists.urls')),
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    #path('tags/', include('tags.urls')),
    path('search/', views.Search, name='search'),
    path('callback/', spotify_callback, name='spotify_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
