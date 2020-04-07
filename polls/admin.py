from django.contrib import admin

# Register your models here.
# 注册模型
# 问题模型
from .models import Question

admin.site.register(Question)