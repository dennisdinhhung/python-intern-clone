from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from articlescraper.models import NewsArticles
from articlescraper.serializers import NewsSerializer, PostNewsSerializer, PutNewsSerializer
from djangoscraper.celery import app as celery_app


class ListNewsArticle(APIView):
    queryset = NewsArticles.objects.all()
    
    def get(self, request):
        search = request.query_params.get('search')
        if search:
            newsarticle = self.queryset.filter(Q(title__icontains=search)|
                                               Q(desc__icontains=search)|
                                               Q(url__icontains=search))
            serializer = NewsSerializer(newsarticle, many=True)
            return Response(serializer.data)
        
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(self.queryset, request)
        serializer = NewsSerializer(page_obj, many=True)
        return Response({
            "total": self.queryset.count(),
            "count": len(serializer.data),
            "data": serializer.data
        })
    
    def post(self, request):
        serializer = PostNewsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                serializer.errors,
                status=400)
            
        title = request.data.get("title")
        desc = request.data.get("desc")
        url = request.data.get("url")
        url_check = self.queryset.filter(url__icontains=url).first()
        if url_check:
            return Response({"message": "url already existed"},status=400)
        
        NewsArticles.objects.create(title=title, desc=desc, url=url)
        entry = self.queryset.filter(url__icontains=url).first()
        return Response(
            {"id": entry.id},
            status=201)
        
    
    def put(self, request, pk):
        entry = NewsArticles.objects.filter(id=pk).first()
        serializer = PutNewsSerializer(entry, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        news = NewsArticles.objects.filter(id=pk).first()
        if not news:
            return Response(serializer.errors, status=400)
        
        NewsArticles.objects.filter(id=pk).update(**serializer.validated_data)
        return Response(status=200)
        
    
    def delete(self, request, pk):
        entry = NewsArticles.objects.filter(id=pk).first()
        #serialize the id 
        if not entry:
            return Response({"message": "Entry not found"}, status=400)
        entry.delete()
        return Response(status=204)

class Scraper(APIView):
    queryset = NewsArticles.objects.all()
    
    def get(self, request):
        celery_app.send_task('celery_scraper')
        return Response(status=200)