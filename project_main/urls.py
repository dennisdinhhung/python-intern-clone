from django.urls import include, path

urlpatterns = [
    path('article/', include('articles.urls')),
    path('auth/', include('authenticator.urls')),
]
