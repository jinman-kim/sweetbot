from django.db import models
from user.models import User


# Create your models here.

class Feed(models.Model):

    def __str__(self):
        return self.author.user_id

    content = models.TextField(blank=True)  # 글내용 (글자 제한 없음)
    image = models.TextField(blank=True, null=True)  # 피드 이미지 (null 값 허용)
    email = models.EmailField(default='no')  # 글쓴이
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feeds',
        null=True, blank=True  # author 필드를 nullable로 변경
    )

    def save(self, *args, **kwargs):
        if self.author is None and self.email:
            # email 값을 이용해 author를 찾거나 생성
            self.author, _ = User.objects.get_or_create(email=self.email)
        super().save(*args, **kwargs)