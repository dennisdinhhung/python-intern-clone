from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from articlescraper.models import NewsArticles
from articlescraper.serializers import DeleteNewsSerializer, NewsSerializer, PostNewsSerializer, PutNewsSerializer
from djangoscraper.celery import app as celery_app


class ListNewsArticle(APIView):
    
    def get(self, request):
        search = request.query_params.get('search')
        if search:
            newsarticle = NewsArticles.objects.filter(Q(title__icontains=search)|
                                                      Q(desc__icontains=search)|
                                                      Q(url__icontains=search))
            serializer = NewsSerializer(newsarticle, many=True)
            return Response(serializer.data)
        
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(NewsArticles.objects.all(), request)
        serializer = NewsSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostNewsSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
            
        title = request.data.get("title")
        desc = request.data.get("desc")
        url = request.data.get("url")
        url_check = NewsArticles.objects.filter(url__icontains=url).first()
        if url_check:
            raise ValidationError("URL already existed")
        
        NewsArticles.objects.create(title=title, desc=desc, url=url)
        entry = NewsArticles.objects.filter(url__icontains=url).first()
        return Response(
            {"id": entry.id},
            status=201)
        
    
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

class Scraper(APIView):
    queryset = NewsArticles.objects.all()
    
    def get(self, request):
        celery_app.send_task('celery_scraper')
        return Response(status=200)

class GetDetail(APIView):
    
    def get(self, request, pk):
        entry = NewsArticles.objects.filter(id=pk).first()
        if not entry:
            raise ValidationError({"message":"Entry does not exists"})
        
        serializer = NewsSerializer(entry)
        return Response(serializer.data)