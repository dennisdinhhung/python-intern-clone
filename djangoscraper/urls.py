from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('article/', include('articlescraper.urls')),
    path('auth/', include('authenticator.urls')),
    path('admin/', admin.site.urls),
]
