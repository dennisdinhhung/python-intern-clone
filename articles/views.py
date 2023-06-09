from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from articles.models import Articles
from articles.serializers import ArticleGetListSerializer, ArticleSerializer, \
    ArticleDeleteSerializer, ArticleUpdateSerializer, \
    ArticleCreateSerializer, ArticleGetSerializer
from project.celery import app as celery_app


class ArticleList(APIView):

    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        return [auth() for auth in self.authentication_classes]

    def get(self, request):
        query_params = request.query_params.dict()
        serializer = ArticleGetListSerializer(data=query_params)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        search = serializer.validated_data.get('search') or ''
        articles = Articles.objects \
            .filter(Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(url__icontains=search))
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        data = serializer.validated_data
        url = data.get("url")
        if Articles.objects.filter(url=url).exists():
            raise ValidationError("Article already existed")
        article = Articles.objects.create(**serializer.validated_data)
        return Response({"id": article.id, "message": "Article create successful."}, status=201)


class ArticleDetail(APIView):

    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        return [auth() for auth in self.authentication_classes]

    def get(self, request, pk):
        serializer = ArticleGetSerializer(data={"id": pk})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        if not Articles.objects.filter(id=pk).exists():
            raise ValidationError({"message": "Article does not exists."})

        article = Articles.objects.filter(id=pk).first()
        output = ArticleSerializer(article).data
        return Response(output)

    def put(self, request, pk):
        serializer = ArticleUpdateSerializer(data={**request.data, 'id': pk})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        article = Articles.objects.filter(id=pk).first()
        if not article:
            raise ValidationError("Article not found.")
        data = serializer.validated_data
        article.title = data.get('title')
        article.description = data.get('description')
        article.url = data.get('url')
        article.save()
        return Response({"message": "Article update successful."}, status=200)

    def delete(self, request, pk):
        serializer = ArticleDeleteSerializer(data={"id": pk})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        article = Articles.objects.filter(id=pk).first()
        if not article:
            raise ValidationError("Article not found.")
        article.delete()
        return Response(status=204)


class ArticleScraper(APIView):

    def get(self, request):
        celery_app.send_task('tasks.article_scraper')
        return Response(status=200)
