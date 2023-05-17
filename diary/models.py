from django.db import models

# Create your models here.

class Feed(models.Model):
    content = models.TextField()        #본문
    image = models.TextField()          #본문 사진
    profile_image = models.TextField()  #프로필 사진
    user_id = models.TextField()        #유저 아이디
    #like_count = models.TextField()     #좋아요 수