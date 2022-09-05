from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from articles.models import Articles
from articles.serializers import ArticleGetListSerializer, ArticleSerializer, ArticleDeleteSerializer, ArticlePostSerializer, ArticlePutSerializer
from project.celery import app as celery_app


class GetListNewsArticle(APIView):
    
    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        
        return [auth() for auth in self.authentication_classes]
    
    def get(self, request):
        query_params = request.query_params.dict()
        serializer = ArticleGetListSerializer(data=query_params)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        search = request.query_params.get('search') or ''
        newsarticle = Articles.objects.filter(Q(title__icontains=search)|
                                              Q(description__icontains=search)|
                                              Q(url__icontains=search))
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(newsarticle, request)
        serializer = ArticleGetListSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ArticlePostSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        validated = serializer.validated_data
        title = validated.get("title")
        description = validated.get("description")
        url = validated.get("url")
        if Articles.objects.filter(url=url).exists():
            raise ValidationError("URL already existed")
        
        article = Articles.objects.create(title=title, description=description, url=url)
        return Response(
            {"id": article.id},
            status=201)

class Scraper(APIView):
    
    def get(self, request):
        celery_app.send_task('celery_scraper')
        return Response(status=200)

class ManageNewsArticle(APIView):
    
    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        
        return [auth() for auth in self.authentication_classes]
    
    def get(self, request, pk):
        #TODO: validate input pk
        if not Articles.objects.filter(id=pk).exists():
            raise ValidationError({"message":"Entry does not exists"})
        
        entry = Articles.objects.filter(id=pk).first()
        serializer = ArticleSerializer(entry)
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = ArticlePutSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        entry = Articles.objects.filter(id=pk)
        if not entry.first():
            raise ValidationError("Entry not found")
        
        entry.update(**serializer.validated_data)
        return Response({"message":" Article update successful."},status=200)
        
    
    def delete(self, request, pk):
        serializer = ArticleDeleteSerializer(data={"id":pk})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        entry = Articles.objects.filter(id=pk).first()
        if not entry:
            raise ValidationError("Entry not found")
        entry.delete()
        return Response(status=204)