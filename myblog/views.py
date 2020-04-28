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
from rest_framework import mixins, authentication
from rest_framework.viewsets import GenericViewSet



#权限管理
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
# 重写返回数据, （谨记只是改了Response对象。）
from common.utils.custom_response import JsonResponse
from rest_framework import status

from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model

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
        
"""3. 获取用户信息(验证token)"""
class getUser(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        print(user)
        return models.User.objects.filter(username=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    # 权限
    # permission_classes = (permissions.AllowAny,) # 所有用户
    # permission_classes = (permissions.IsAuthenticated,) # 登陆成功的token
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) # 登陆成功的token,只能读操作
    # permission_classes = (permissions.IsAdminUser,) # 登陆成功的管理员token


# def get_user_info(request):

#     User = get_user_model()
#     if request.method=='GET':
#         #获取请求参数token的值
#         token=request.GET.get('token')
#         #顶一个空数组来接收token解析后的值
#         toke_user = []
#         toke_user = jwt_decode_handler(token)
#         #获得user_id
#         user_id = toke_user["user_id"]
#         #通过user_id查询用户信息
#         user_info = User.objects.get(pk= user_id)
#         serializer = serializers.UserDetailSerializer(user_info)
#         return JsonResponse(data=serializer.data,msg="success",code=201,status=status.HTTP_201_CREATED,headers=headers)

# class UserViewset(mixins.CreateModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   GenericViewSet):
#     """
#     用户create,update,retrieve时向此view请求
#     """
#     queryset = models.User.objects.all()
#     # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
#     authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

#     # 如果用permission_classes定义访问权限认证IsAuthenticated已登录(否则401)
#     # 那么对这个整个用户视图都生效,但用户在注册时肯定不能在"已登录"状态下
#     # 所以将permission以动态的方式定义
#     def get_permissions(self):
#         """覆写,以在不同的请求方法下使用不同的权限认证"""
#         if self.action == "retrieve":
#             return [permissions.IsAuthenticated()]  # 在已登录的状态下才能访问retrieve(访问自己的信息)
#         elif self.action == "create":
#             return [permissions.AllowAny()]  # 登录/没登录都允许
#         return []  # 使用空数组也和仅有AllowAny()一样的

#     def create(self, request, *args, **kwargs):
#         """
#         用户注册(注意username填写手机号)
#         覆写,以将token加入response给用户(实现注册完自动登录)
#         """
#         serializer = self.get_serializer(data=request.data)
#         # Serializer中做验证并可能抛出异常,出错时将自动返回相应的HTTP状态码
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)
#         print("用户保存化好了")
#         re_dict = serializer.data
#         payload = jwt_payload_handler(user)
#         re_dict["token"] = jwt_encode_handler(payload)
#         re_dict["name"] = user.name if user.name else user.username
#         print("返回的字典做好了")
#         headers = self.get_success_headers(serializer.data)
#         return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         """覆写,将user返回以在create里能取到"""
#         return serializer.save()

#     # 该方法在GET(retrieve)和DELETE(destroy)和PUT(update)时都调用,但对用户而言仅应能操作自己这个用户
#     def get_object(self):
#         """覆写,不管传什么id,都只返回当前用户"""
#         return self.request.user

#     def get_serializer_class(self):
#         """覆写,在不同的请求下做不同的序列化"""
#         if self.action == "retrieve":
#             return serializers.UserDetailSerializer  # 用户详情用
#         elif self.action == "create":
#             return serializers.UserSerializer  # 用户注册用
#         return serializers.UserDetailSerializer

#     def retrieve(self, request, *args, **kwargs):
#         """获取本用户信息(需身份验证,id无论提供多少,仅返回本用户的信息)"""
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         # 获取该用户关注的用户数,以及该用户被多少用户关注(粉丝数)
#         follow_num = Watch.objects.filter(uper=instance.id).count()
#         follower_num = Watch.objects.filter(base=instance.id).count()
#         res = {}
#         for k in serializer.data:
#             res[k] = serializer.data[k]
#         res["follow_num"] = follow_num
#         res["follower_num"] = follower_num
#         return Response(res)

#     def update(self, request, *args, **kwargs):
#         """更新本用户信息(需身份验证,id无论提供多少,仅更新本用户的信息)"""
#         return super().update(request, args, kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         """部分更新,只更新提供的字段(需身份验证,id无论提供多少,仅更新本用户的信息)"""
#         kwargs['partial'] = True
#         # 因为用户名是必填项目,在部分更新时为了不要求提供,直接从authorization中取用
#         if "username" not in request.data.keys():
#             request.data.update({"username": self.request.user.username})
#         return self.update(request, *args, **kwargs)


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

#继承的类重写了父类的方法，这里和mixin类并用可用来给通用视图继承，
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

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 过滤器
    filter_backends = [filters.SearchFilter]
    # 可以在元组中写多个进行筛选。
    search_fields = ['title', 'desc', 'content','user__username','category__name']

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


# 创建文章
class createArticle(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.createArticleSerializer

# 文章详情
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

# 分类列表
class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)
