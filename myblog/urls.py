from django.urls import path

from . import views

# 注册方法：1.路由，2.视图方法。
urlpatterns = [
    # ex: /polls/
    # path('', views.index, name='index'),
    path('articles/', views.ArticleList.as_view()),
    path('articles/<int:pk>/', views.ArticleDetail.as_view()),
]