from rest_framework import serializers
from . import models

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ("__all__")
#         model = models.Article

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


