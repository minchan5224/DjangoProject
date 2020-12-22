from django.contrib.auth.models import User
from django.db import models
from articleapp.models import Article
from commentapp.models import Comment

class Recomment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # related_name='recomment'  Article.recomment 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 Article.pk 랑 했음 article = Article.pk
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # on_delete=models.SET_NULL 회원 탈퇴시 게시글이 사라지는 것이 아닌 주인이 없는 게시글로 되도록
    # related_name='recomment'  user.recomment 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 User.pk 랑 했음 writer = User.pk
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # 외래키 이용 Comment.pk 랑 했음 comment = Comment.pk
    content = models.TextField(null=False)

    create_at = models.DateTimeField(auto_now=True)