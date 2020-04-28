from rest_framework import serializers
from . import models

from drf_dynamic_fields import DynamicFieldsMixin

#获取用户详情
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ("__all__")
#         model = models.Article

"""2. 新增玩家"""
class UserSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username","password",]
    def create(self, validated_data):
        user= models.User.objects.create_user(**validated_data) # 这里新增玩家必须用create_user,否则密码不是秘文
        return user

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ("__all__")
#         model = models.User

# User = get_user_model()
# class UserRegisterSerializer(serializers.ModelSerializer):
#     # 利用drf中的validators验证username是否唯一
#     username = serializers.CharField(required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(),
#                                                                                         message='用户已经存在')])
#     print(username)
#     password = serializers.CharField(
#          style={"input_type": "password"},help_text="密码", label="密码", write_only=True,
#      )
#     print(password, "password")

#     def create(self, validated_data):
#          user = super(UserRegisterSerializer, self).create(validated_data= validated_data)
#          user.set_password(validated_data["password"])
#          user.save()
#          return user
#     class Meta:
#          model = User
#          fields = ( "username", "password", "role", "avatar")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """
    class Meta:
        model = models.User
        fields = ('id','username','email','avatar','qq','mobile','url')

class ArticleSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username")
    avatar_link = serializers.CharField(source="user.avatar")
    # category = serializers.CharField(source="category.name")

    # avatar_link = serializers.serializerMethodField()

    class Meta:


        fields = (
            'id', 
            'avatar_link',
            'title',
            'desc', 'content', 'user','category')
        model = models.Article

    # def get_avatar_link(self, instence):
    #     request = self.context.get("request")
    #     return f"{request.scheme}://{request.get_host()}/{reinstence.pk}"

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Tag
        fields = ("__all__")

class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    date_publish = serializers.DateTimeField(format="%Y-%m-%d %X")
    # 嵌套
    tag = TagSerializer(many=True)
    # tag = serializers.ManyToManyField(source="tag.name")
    
    class Meta:
        fields = ("__all__")
        model = models.Article

class createArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("__all__")
        model = models.Article


class CommentsSerializer(serializers.ModelSerializer):
    date_publish = serializers.DateTimeField(format="%Y-%m-%d %X")
    avatar_link = serializers.CharField(source="user.avatar")
    user = serializers.CharField(source="user.username")
    class Meta:
        model = models.Comment
        fields = ('id','username','content','avatar_link','date_publish','user','article','pid')


# class CommentDetailSerializer(serializers.ModelSerializer):
#     avatar_link = serializers.CharField(source="user.avatar")
#     date_publish = serializers.DateTimeField(format="%Y-%m-%d %X")
#     user = serializers.CharField(source="user.username")
#     class Meta:
#         fields = ('username','content','avatar_link','date_publish','user','article','pid')
#         model = models.Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('__all__')