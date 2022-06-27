from rest_framework import serializers
from articlescraper.models import News

class NewsSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'desc', 'url']
