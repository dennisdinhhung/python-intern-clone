from rest_framework import serializers
from articlescraper.models import News

class NewsSeralizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField()
    url = serializers.CharField(max_length=200)
    # class Meta:
    #     model = News
    #     fields = ['id', 'title', 'desc', 'url']
