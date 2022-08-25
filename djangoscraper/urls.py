from django.urls import include, path

urlpatterns = [
    path('article/', include('articlescraper.urls')),
    path('auth/', include('authenticator.urls')),
]
