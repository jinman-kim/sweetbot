from django.db import models

# Create your models here.

class Feed(models.Model):
    content = models.TextField(blank=True)  # 글내용 (글자 제한 없음)
    image = models.TextField(blank=True, null=True)  # 피드 이미지 (null 값 허용)
    email = models.EmailField(default='')  # 글쓴이
