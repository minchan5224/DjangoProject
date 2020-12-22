from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # OneToOneField는 1:1관계를 의미한다.
    # on_delete=model.CASCADE 탈퇴하면 프로필도 함께 삭제되도록 하는것.
    # related_name='profile' 이건 requset.user.profile를 통해 바로 연결 가능하도록 설정 해주는것
    # 따로 프로필 객체를 찾을 필요가 없다.
    image = models.ImageField(upload_to='profile/', null=True)
    # 이미지를 받아서 서버 내부의 어느곳에 저장될 것인지 경로를 정해주는것.
    # null=True 는 프로필 사진이 없어도 된다는 뜻.
    nickname = models.CharField(max_length=12, unique=True, null=True)
    # unique=True 닉네임 중복 불허
    message = models.CharField(max_length=100, null=True)
    # 대화명
