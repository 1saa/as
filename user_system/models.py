from django.db import models

# Create your models here.
class User(models.Model):
    
    username        = models.CharField(max_length=16, unique=True, db_index=True)
    email           = models.EmailField()
    password_hash   = models.CharField(max_length=16)
    profile         = models.TextField(default="not edit yet")
    like_users      = models.CharField(max_length=512, null=True) #json字符串 string符列表
    like_tags       = models.CharField(max_length=512, null=True) #json字符串 string符列表

    class Meta:
        abstract = True

class Normal_user(User):
    public          = models.BooleanField(default=0)

class Admin_user(User):
    public          = models.BooleanField(default=1)

class Papers(models.Model):

    name            = models.CharField(max_length=128, db_index=True)
    information     = models.TextField(default="Please edit by yourselves")
    authors         = models.CharField(max_length=128) #json字符串，string列表，初始包含创始的管理员
    file            = models.FileField(upload_to='paper_file/')
    tag_list        = models.CharField(max_length=512) #json list，初始包含自己的name作为tag
    create_time     = models.DateField(auto_now_add=True)
    last_edit_time  = models.DateTimeField(null=True)

class Discussion(models.Model):

    creater         = models.CharField(max_length=16, db_index=True)
    title           = models.CharField(max_length=128, db_index=True)
    information     = models.TextField()
    tag_list        = models.CharField(max_length=512) #json list
    recommend       = models.IntegerField(default=0)
    reply           = models.TextField(default='There is no reply')
    reply_number    = models.IntegerField(default=0)
    create_time     = models.DateField(auto_now_add=True)
    last_reply      = models.CharField(max_length=512, null=True)
    last_name       = models.CharField(max_length=16, null=True)
    last_time       = models.DateTimeField(null=True)

class Dis_center(models.Model):

    tag_title   = models.CharField(max_length=128, db_index=True)
    number      = models.IntegerField(default=1)