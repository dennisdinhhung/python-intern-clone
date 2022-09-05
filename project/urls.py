from django.urls import include, path

urlpatterns = [
    path('articles/', include('articles.urls')),
    path('auth/', include('authenticator.urls')),
]
