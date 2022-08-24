from rest_framework import serializers

class NewsSerializer(serializers.Serializer):
    
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=200)

class PostNewsSerializer(serializers.Serializer):
    
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=200)
    
#put
class PutNewsSerializer(serializers.Serializer):
    
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=200)

#del
class DeleteNewsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()

#get a specific entry using the id
class DetailedNewsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=200)