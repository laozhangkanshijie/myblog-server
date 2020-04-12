from rest_framework import serializers
from . import models

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title','desc', 'content', 'click_count','is_recommend','date_publish', 'user','category','tag')
        model = models.Article