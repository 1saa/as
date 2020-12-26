from django.db import models
from django.utils import timezone
import json

# Create your models here.
class User(models.Model):
    
    username        = models.CharField(max_length=16, unique=True, db_index=True)
    email           = models.EmailField(null=True)
    password_hash   = models.CharField(max_length=32)
    profile         = models.TextField(default="not edit yet")
    like_users      = models.JSONField(default=list)
    like_tags       = models.JSONField(default=list)
    is_admin        = models.BooleanField(default=0)
    public          = models.BooleanField(default=1)

    def edit_email(self, em):
        self.email = em
        self.save()
    
    def edit_password(self, ps):
        self.password_hash = ps
        self.save()

    def edit_profile(self, text):
        self.profile = text
        self.save()
    
    def add_like_user(self, name):
        if not name in self.like_users:
            self.like_users.append(name)
            self.save()
    
    def delete_like_user(self, name):
        if name in self.like_users:
            self.like_users.remove(name)
            self.save()
        
    def add_like_tags(self, name):
        if not name in self.like_tags:
            self.like_tags.append(name)
            self.save()
    
    def delete_like_tags(self, name):
        if name in self.like_tags:
            self.like_tags.remove(name)
            self.save()

    def edit_pri(self, u):
        if self.is_admin == True:
            self.public = 1
        else:
            self.public = u
        self.save()

class Papers(models.Model):

    name            = models.CharField(max_length=128, unique=True, db_index=True)
    pubyear         = models.CharField(max_length=10, default="unknown")
    publisher       = models.JSONField(default=list)
    information     = models.TextField(default="Please edit by yourselves")
    admins          = models.JSONField(default=list)
    file            = models.URLField(default='file\\0.pdf')
    tag_list        = models.JSONField(default=list)
    create_time     = models.DateField(auto_now_add=True)
    last_name       = models.CharField(max_length=16, null=True)
    last_time       = models.DateTimeField(null=True)

    def add_tag(self, tag):
        if tag not in self.tag_list:
            self.tag_list.append(tag)
            self.save()

    def delete_tag(self, tag):
        if tag in self.tag_list:
            self.tag_list.remove(tag)
            self.save()

    def edit_info(self, text, name):
        self.information = text
        self.last_name = name
        self.last_time = timezone.now()
        self.save()

class Discussion(models.Model):

    creator         = models.CharField(max_length=16, db_index=True)
    title           = models.CharField(max_length=128, db_index=True)
    tag_list        = models.JSONField(default=list)
    paper_list      = models.JSONField(default=list)
    reply           = models.JSONField(default=list)
    reply_number    = models.IntegerField(default=0)
    create_time     = models.DateField(auto_now_add=True)
    last            = models.JSONField(default=dict)
    last_time       = models.DateTimeField(null=True)

    def add_tag(self, tag):
        if tag not in self.tag_list:
            self.tag_list.append(tag)
            self.save()

    def delete_tag(self, tag):
        if tag in self.tag_list:
            self.tag_list.remove(tag)
            self.save()

    def add_reply(self, to, text, name):
        self.reply_number += 1
        self.last['to'] = to
        self.last['text'] = text
        self.last['name'] = name
        self.last['time'] = timezone.now().strftime("%Y-%m-%d, %H:%M:%S")
        self.last['reconumb'] = 0
        self.last['recolist'] = [] 
        self.reply.append(self.last)
        self.last_time = timezone.now()
        self.save()

class DisCenter(models.Model):

    tag_title   = models.CharField(max_length=128, unique=True, db_index=True)
    number      = models.IntegerField(default=0)
    dis_list    = models.JSONField(default=list)