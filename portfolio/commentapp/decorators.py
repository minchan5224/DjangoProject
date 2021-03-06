from django.http import HttpResponseForbidden
from commentapp.models import Comment

def comment_ownership_required(func):
    def decorated(request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 profile이 된다.
        if not comment.writer == request.user: #그 article request의 profile이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)
    return decorated