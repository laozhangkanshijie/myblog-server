from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

class ArticleList(generics.ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

class ArticleDetail(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer