from django.db import models
from user.models import User

# Create your models here.

class Feed(models.Model):
    
    content = models.TextField(blank=True)  # 글내용 (글자 제한 없음)
    image = models.TextField(blank=True, null=True)  # 피드 이미지 (null 값 허용)
    email = models.EmailField(default='no') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds', 
                             null=True, blank=True, to_field='user_id')

    def save(self, *args, **kwargs):
        if not self.user_id and self.email:
            self.user, _ = User.objects.get_or_create(email=self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        print("에러")
        return self.user.user_id
