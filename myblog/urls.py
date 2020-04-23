from django.urls import path
from django.urls import path,include
from rest_framework import routers
from . import views
createUserViewRouter = routers.DefaultRouter() # 新增用户
createUserViewRouter.register('', views.createUser,)
getUserRouter = routers.DefaultRouter() # 查看用户列表
getUserRouter.register('', views.getUser,)

# 注册方法：1.路由，2.视图方法。
urlpatterns = [
    # ex: /polls/
    # path('', views.index, name='index'),
    path('articles/', views.ArticleList.as_view()),
    path('articles/<int:pk>/', views.ArticleDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    # path('comments/<int:pk>/', views.CommentDetail.as_view()),
    # path('user/', views.UserListView.as_view()),
    # path('index/', views.Index.as_view()),
    path('gettoken/',views.loginView.as_view()), # 获取 token
    path('createuser/',include(createUserViewRouter.urls)), # 新增用户
    path('getuser/',include(getUserRouter.urls)), # 获取用户
]