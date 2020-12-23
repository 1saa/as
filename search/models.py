from django.db import models
import json


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=16, unique=True, db_index=True)
    email = models.EmailField(null=True)
    password_hash = models.CharField(max_length=16)
    profile = models.TextField(default="not edit yet")
    like_users = models.JSONField(default=list)
    like_tags = models.JSONField(default=list)
    is_admin = models.BooleanField(default=0)
    public = models.BooleanField(default=1)

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
    name = models.CharField(max_length=128, db_index=True)
    information = models.TextField(default="Please edit by yourselves")
    authors = models.JSONField(default=list)
    file = models.FileField(upload_to='paper_file/')
    tag_list = models.JSONField(default=list)
    create_time = models.DateField(auto_now_add=True)
    last_edit_time = models.DateTimeField(null=True)


class Discussion(models.Model):
    creater = models.CharField(max_length=16, db_index=True)
    title = models.CharField(max_length=128, db_index=True)
    information = models.TextField()
    tag_list = models.JSONField(default=list)
    recommend = models.IntegerField(default=0)
    reply = models.TextField(default='There is no reply')
    reply_number = models.IntegerField(default=0)
    create_time = models.DateField(auto_now_add=True)
    last_reply = models.CharField(max_length=512, null=True)
    last_name = models.CharField(max_length=16, null=True)
    last_time = models.DateTimeField(null=True)


class Dis_center(models.Model):
    tag_title = models.CharField(max_length=128, db_index=True)
    number = models.IntegerField(default=1)