from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import pagination

from . import models
from . import serializers
# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

class ArticleList(generics.ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    # 过滤器
    filter_backends = (filters.SearchFilter, )
    # 可以在元组中写多个进行筛选。
    search_fields = ("desc",)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code":0,
                "data": serializer.data
            }
        )

class ArticleList(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

class ArticleDetail(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer



class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer