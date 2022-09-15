from django.urls import include, path

urlpatterns = [
    path('v1/articles/', include('articles.urls')),
    path('v1/auth/', include('authenticator.urls')),
]
