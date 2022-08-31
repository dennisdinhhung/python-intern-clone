from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from articles.models import NewsArticles
from articles.serializers import DeleteNewsSerializer, NewsSerializer, PostNewsSerializer, PutNewsSerializer
from project_main.celery import app as celery_app


class GetListNewsArticle(APIView):
    
    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        
        return [auth() for auth in self.authentication_classes]
    
    def get(self, request):
        search = request.query_params.get('search') or ''
        newsarticle = NewsArticles.objects.filter(Q(title__icontains=search)|
                                                  Q(description__icontains=search)|
                                                  Q(url__icontains=search))
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(newsarticle, request)
        serializer = NewsSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostNewsSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        print("data")
        print(type(serializer.data))
        print("validated_data")
        print(type(serializer.validated_data))
        
        validated = serializer.validated_data
        title = validated.get("title")
        description = validated.get("description")
        url = validated.get("url")
        url_check = NewsArticles.objects.filter(url__icontains=url).first()
        if url_check:
            raise ValidationError("URL already existed")
        
        NewsArticles.objects.create(title=title, description=description, url=url)
        entry = NewsArticles.objects.filter(url__icontains=url).first()
        return Response(
            {"id": entry.id},
            status=201)

class Scraper(APIView):
    queryset = NewsArticles.objects.all()
    
    def get(self, request):
        celery_app.send_task('celery_scraper')
        return Response(status=200)

class ManageNewsArticle(APIView):
    
    def get(self, request, pk):
        entry = NewsArticles.objects.filter(id=pk).first()
        if not entry:
            raise ValidationError({"message":"Entry does not exists"})
        
        serializer = NewsSerializer(entry)
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = PutNewsSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        entry = NewsArticles.objects.filter(id=pk)
        if not entry.first():
            raise ValidationError("Entry not found")
        
        entry.update(**serializer.validated_data)
        return Response(status=200)
        
    
    def delete(self, request, pk):
        serializer = DeleteNewsSerializer(data={"id":pk})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        entry = NewsArticles.objects.filter(id=pk).first()
        if not entry:
            raise ValidationError("Entry not found")
        entry.delete()
        return Response(status=204)