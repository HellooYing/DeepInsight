from django.contrib.auth.models import AbstractUser
from django.db import models
import time

# class User(models.Model):
#     name = models.CharField('真实姓名',max_length=50,)
#     email = models.EmailField('邮箱',max_length=50,primary_key=True,null=False)
#     phone = models.CharField('电话',max_length=11,null=False)
#     password = models.CharField('密码',max_length=30)
#     unit = models.CharField('单位',max_length=30,null=False)
#     office = models.CharField('科室',max_length=50,null=False)
#     post = models.CharField('职务',max_length=50,null=False)
#     professional = models.CharField('职称',max_length=50,null=False)
#     number = models.CharField('工号',max_length=50,null=False)
from license import settings


class User(AbstractUser):

    id = models.IntegerField(auto_created=True,primary_key=True)
    username = models.CharField('邮箱/电话号码',max_length=50,unique=True,null=False)
    name = models.CharField('真实姓名',max_length=50)
#   phone = models.CharField('电话',max_length=11,null=False)
    unit = models.CharField('单位',max_length=30,null=False)
    office = models.CharField('科室',max_length=50,null=False)
    post = models.CharField('职务',max_length=50,null=False)
    professional = models.CharField('职称',max_length=50,null=False)
    number = models.CharField('工号',max_length=50,null=False)
    isadmin = models.BooleanField('是否为管理员',default=False)
# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    user_image=models.ImageField('个人')

class History(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True)
    apply_time = models.DateTimeField('申请日期',max_length=50,auto_now = True)
    ratify_time = models.DateTimeField('批准日期',max_length=50, auto_now = True)
    limit_time = models.DateTimeField('有效时间',max_length=50)
    activation = models.CharField('激活码',max_length=50,default='待发放')
    SNnum = models.CharField('SN号',default='待发放',max_length=50)
    examine = models.CharField('审核',default='未审核',max_length=50)#审核通过/审核未通过
    pass_or_not = models.NullBooleanField('是否通过',default='')
