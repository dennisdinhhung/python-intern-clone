from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from articlescraper.models import News
from articlescraper.scraper import scrape
from articlescraper.serializers import NewsSerializer, PostNewsSerializer
from djangoscraper.celery import app as celery_app

class ListNewsArticle(APIView):
    
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404
    
    def get(self, request):
        queryset = News.objects.all()
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(queryset, request)
        serializer = NewsSerializer(page_obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostNewsSerializer(data=request.data)
        if serializer.is_valid():
            title = request.data.get("title")
            desc = request.data.get("desc")
            url = request.data.get("url")
            News.objects.create(title=title, desc=desc, url=url)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        entry = self.get_object(pk)
        serializer = PostNewsSerializer(entry, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        news = News.objects.filter(id=pk).first()
        if not news:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        News.objects.filter(id=pk).update(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
        
    
    def delete(self, request, pk):
        if not News.objects.filter(id=pk).first():
            return Response({"message": "Entry not found"}, status=status.HTTP_400_BAD_REQUEST)
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Scraper(APIView):
    queryset = News.objects.all()
    
    def get(self, request):
        celery_app.send_task('celery_scraper')
        return Response(status=status.HTTP_200_OK)
    
class Search(APIView):
    queryset = News.objects.all()
    
    def get(self, request):
        title = request.query_params.get('title')
        if title:
            newsarticle = self.queryset.filter(title__icontains=title)
            serializer = NewsSerializer(newsarticle, many=True)
        return Response(serializer.data)