from rest_framework import serializers
from newsscraper.models import News

class NewsSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'desc', 'url']