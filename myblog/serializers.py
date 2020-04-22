from rest_framework import serializers
from . import models

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ("__all__")
#         model = models.Article

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("__all__")
        model = models.User

class ArticleSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username")
    avatar_link = serializers.CharField(source="user.avatar")

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