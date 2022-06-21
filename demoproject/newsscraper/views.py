from django.shortcuts import render
from django.http import HttpResponse
from .scraper import scrape
from .models import News

def index(request):
    list = scrape()
    
    for item in list:
        title = item["title"]
        desc = item["desc"]
        
        News.objects.create(title=title, desc=desc)
        
    return HttpResponse(list)