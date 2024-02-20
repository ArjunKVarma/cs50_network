from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    pass
    # followers = ArrayField(models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True))



class Post(models.Model):
    content = models.CharField(max_length=2000)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField()
    active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner} : {self.content},  {self.date}"

class Follow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE , related_name = "creator")
    follower = models.ForeignKey(User, on_delete=models.CASCADE , related_name = "follower")

class Like(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    