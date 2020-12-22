from django.db import models
from django.contrib.auth.models import User
from articleapp.models import Article


class Articlelike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_like')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_like')

    class Meta:
        unique_together = ('user', 'article')

class ArticleUnlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_Unlike')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_Unlike')

    class Meta:
        unique_together = ('user', 'article')
