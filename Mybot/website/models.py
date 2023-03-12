from django.db import models
from django.contrib.auth.models import User


class PreviousChat(models.Model):
    question = models.CharField(max_length=5000)
    answer = models.TextField(max_length=7000)
    history_str = models.TextField(max_length=10000)
    created_time = models.DateTimeField(auto_now_add=True)
    # 增加owner字段，建立到模型User的外键关系
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
