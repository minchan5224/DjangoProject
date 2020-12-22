from django.contrib.auth.models import User
from django.db import models
from projectapp.models import Project

class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='article', null=True)
    # on_delete=models.SET_NULL 회원 탈퇴시 게시글이 사라지는 것이 아닌 주인이 없는 게시글로 되도록
    # related_name='article'  user.article로 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 User.pk 랑 했음 writer = User.pk
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='article', null=True)
    # related_name='article'  Project.article로 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 Project.pk 랑 했음 project = Project.pk
    title = models.CharField(max_length=200, null=True)
    # 제목없음 가능
    image = models.ImageField(upload_to='article/', null=False)
    content = models.TextField(null=True)
    # 내용이 좀 긴 경우 대비해서 textfield 사용
    created_at = models.DateTimeField(auto_created=True, null=True)
    # 게시글 작성 시간 표시, auto_created=True 쓰면 자동으로 함