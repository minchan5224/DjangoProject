from django.http import HttpResponseForbidden
from recommentapp.models import Recomment

def Recomment_ownership_required(func):
    def decorated(request, *args, **kwargs):
        recomment = Recomment.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 profile이 된다.
        if not recomment.writer == request.user: #그 article request의 profile이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)
    return decorated