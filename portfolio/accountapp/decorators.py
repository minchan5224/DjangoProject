from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 user이 된다.
        if not user == request.user: #그 user이 request의 abs()이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)

    return decorated