from rest_framework import generics
from rest_framework.response import Response

from rest_framework import filters
from rest_framework import pagination

from rest_framework.views import APIView
from rest_framework import status

from . import models
from . import serializers
# 登录验证
from . import jwtMiddleware
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import Http404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
#权限管理
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
# 重写返回数据, （谨记只是改了Response对象。）
from common.utils.custom_response import JsonResponse
from rest_framework import status



#筛选过滤
from django_filters.rest_framework import DjangoFilterBackend

class createUser(mixins.CreateModelMixin,GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

"""1. 登陆"""
class loginView(APIView):
    """登陆成功后,获取TOKEN"""
    def post(self,request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if not user:
            raise Http404("账号密码不匹配")
        login(request, user)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # return Response({ "success": True, "msg": "登录成功","results": token},status=status.HTTP_200_OK)
        return JsonResponse(data={"token": token},code=200,msg="success",status=status.HTTP_200_OK)
        
"""3. 获取用户列表(验证token)"""
class getUser(mixins.ListModelMixin,GenericViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    # 权限
    # permission_classes = (permissions.AllowAny,) # 所有用户
    # permission_classes = (permissions.IsAuthenticated,) # 登陆成功的token
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) # 登陆成功的token,只能读操作
    # permission_classes = (permissions.IsAdminUser,) # 登陆成功的管理员token

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

# class UserListView(generics.ListAPIView):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserSerializer
    # filter_backends = [DjangoFilterBackend]

class CommentList(generics.ListAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentsSerializer

    # 过滤器
    filter_backends = [DjangoFilterBackend,]
    # 可以在元组中写多个进行筛选。
    filterset_fields = ['article','pid']

    def list(self, request):
        #  !!!记得下面这句代码很重要！！！
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.CommentsSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

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
    # authentication_classes = [jwtMiddleware.TokenAuth,]

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



# class CommentDetail(generics.RetrieveAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializers.CommentDetailSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)
