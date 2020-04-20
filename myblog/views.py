# from django.shortcuts import render
# generics
from rest_framework import generics
from rest_framework.response import Response

from rest_framework import filters
from rest_framework import pagination

from . import models
from . import serializers
# Create your views here.
# def index(request):
#     return render(request, 'index.html', locals())

# 获取所有文章列表
class ArticleList(generics.ListAPIView):
    # queryset 为查询实例
    queryset = models.Article.objects.all()
    # 使用自己定义的文章序列化器
    serializer_class = serializers.ArticleSerializer

    # 过滤器
    filter_backends = [filters.SearchFilter]
    # 可以在元组中写多个进行筛选。
    search_fields = ['title', 'desc', 'content']

    # 分页器
    pagination_class = pagination.LimitOffsetPagination

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({
    #         "code": 0,
    #         "data": serializer.data,
    #         # "search_fields": self.search_fields
    #     })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 实现分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 调用serializer.data静态方法，得到python数据类型
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code":0,
                "data": serializer.data
            }
        )

    def get_paginated_response(self, data):
        return Response(
            {
                "code":0,
                "data":{
                    "total": self.paginator.count,
                    "data": data
                }
            }
        )

# class ArticleList(generics.ListCreateAPIView):
#     queryset = models.Article.objects.all()
#     serializer_class = serializers.ArticleSerializer

class ArticleDetail(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 0,
            "data": serializer.data,
            # "search_fields": self.search_fields
        })



# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Article.objects.all()
#     serializer_class = serializers.ArticleDetailSerializer