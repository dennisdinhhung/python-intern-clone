from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    url = serializers.CharField(max_length=1000)
    
class ArticleGetListSerializer(serializers.Serializer):
    search = serializers.CharField(default=None, required=False, max_length=255, allow_blank=True)

class ArticlePostSerializer(serializers.Serializer):
    
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    url = serializers.CharField(max_length=1000)
    
class ArticlePutSerializer(serializers.Serializer):
    
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    url = serializers.CharField(max_length=1000)
    
class ArticleDeleteSerializer(serializers.Serializer):
    
    id = serializers.UUIDField()

class ArticleGetDetailSerializer(serializers.Serializer):
    
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    url = serializers.CharField(max_length=1000)