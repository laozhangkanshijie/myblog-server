from rest_framework import generics
from rest_framework.response import Response

from rest_framework import filters
from rest_framework import pagination

from . import models
from . import serializers
# 登录验证
from . import jwtMiddleware
# 重写返回数据, （谨记只是改了Response对象。）
from common.utils.custom_response import JsonResponse
from rest_framework import status


# 重写返回数据
# from . import serializers
# from . import models
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from django.shortcuts import get_object_or_404
# from common.utils.custom_response import  JsonResponse
# from rest_framework import filters
# from django_filters import rest_framework
# from django_filters.rest_framework import DjangoFilterBackend


# class CustomViewBase(viewsets.ModelViewSet):
#     # pagination_class = LargeResultsSetPagination
#     # filter_class = ServerFilter
#     queryset = ''
#     serializer_class = ''
#     permission_classes = ()
#     filter_fields = ()
#     search_fields = ()
#     filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return JsonResponse(data=serializer.data,msg="success",code=201,status=status.HTTP_201_CREATED,headers=headers)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             # 调用serializer.data静态方法，得到python数据类型
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return JsonResponse(data=serializer.data,code=200,msg="success",status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return JsonResponse(data=serializer.data,code=200,msg="success",status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return JsonResponse(data=serializer.data,msg="success",code=200,status=status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return JsonResponse(data=[],code=204,msg="delete resource success",status=status.HTTP_204_NO_CONTENT)



# 获取所有文章列表
class ArticleList(generics.ListAPIView):
    # queryset 为查询实例
    queryset = models.Article.objects.all()
    # 使用自己定义的文章序列化器
    serializer_class = serializers.ArticleSerializer

    # 过滤器
    filter_backends = [filters.SearchFilter]
    # 可以在元组中写多个进行筛选。
    search_fields = ['title', 'desc', 'content','user__username']

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

    # 局部认证的配置
    authentication_classes = [jwtMiddleware.TokenAuth,]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 实现分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 调用serializer.data静态方法，得到python数据类型
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def get_paginated_response(self, data):
        return JsonResponse(data={
            "total": self.paginator.count,
            "data": data
        }, code=200, msg="success", status=status.HTTP_200_OK)


# class ArticleList(generics.ListCreateAPIView):
#     queryset = models.Article.objects.all()
#     serializer_class = serializers.ArticleSerializer

class ArticleDetail(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Article.objects.all()
#     serializer_class = serializers.ArticleDetailSerializer
