from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articlescraper import serializers
from articlescraper.models import News

from articlescraper.scraper import scrape
from articlescraper.serializers import NewsSeralizer

class ListNewsArticle(APIView):  
    queryset = News.objects.all()
    permission_classes = []
    
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404
    
    def get(self, request):
        queryset = News.objects.all()
        serializer = NewsSeralizer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = NewsSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        entry = self.get_object(pk)
        serializer = NewsSeralizer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Scraper(APIView):
    queryset = News.objects.all()
    
    def get(self, request):
        list = scrape()
    
        for item in list:
            title = item["title"]
            desc = item["desc"]
            url = item['url']
        
            News.objects.create(title=title, desc=desc, url=url)
        
        return HttpResponse(list)