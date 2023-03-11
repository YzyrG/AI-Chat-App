from django.db import models


class PreviousChat(models.Model):
    question = models.CharField(max_length=5000)
    answer = models.TextField(max_length=7000)

    def __str__(self):
        return self.question
