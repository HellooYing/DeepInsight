from django.contrib.auth.models import AbstractUser
from django.db import models


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

class User(AbstractUser):

    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField('真实姓名',max_length=50)
    username = models.EmailField('邮箱',max_length=50,unique=True,null=False)
    phone = models.CharField('电话',max_length=11,null=False)
    unit = models.CharField('单位',max_length=30,null=False)
    office = models.CharField('科室',max_length=50,null=False)
    post = models.CharField('职务',max_length=50,null=False)
    professional = models.CharField('职称',max_length=50,null=False)
    number = models.CharField('工号',max_length=50,null=False)
# Create your models here.
