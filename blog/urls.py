"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path,re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
from django.views.generic.base import TemplateView
# 获取JWT的token用
from rest_framework_jwt.views import obtain_jwt_token
from myblog import views
from rest_framework.routers import DefaultRouter

# suersViewRouter = DefaultRouter()
# suersViewRouter.register('', views.UserViewset, )

urlpatterns = [
    # path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    # path('login/', obtain_jwt_token),
    # path('api/', include('blog_api.urls')),
    path('api/', include('myblog.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
    # path('index/', views.Index.as_view()),
    # re_path('api/user/info/$', views.get_user_info),
    # path('users/',include(suersViewRouter.urls)), # 新增用户
    
]
