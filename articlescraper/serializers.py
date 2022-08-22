from rest_framework import serializers

class NewsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField()
    url = serializers.CharField(max_length=200)

class PostNewsSerializer(serializers.Serializer):
    
    url = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)