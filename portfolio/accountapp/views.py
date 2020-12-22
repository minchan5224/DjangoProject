from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth # 로그인

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accountapp.decorators import account_ownership_required

from articleapp.models import Article
from django.views.generic.list import MultipleObjectMixin
has_ownership = [account_ownership_required, login_required]
# 본인확인, 로그인 여부 확인 과정
# 리스트로 담아서 사용 가능하다.

class AccountCreateView(View):
    def post(self, request):
        user_id = request.POST.get('username',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)

        if User.objects.filter(username = user_id).exists() == True:
            message = "이미 존재하는 아이디입니다."

        elif password != re_password:
            message = "비밀번호가 다릅니다."

        elif user_id == '' or password == '':
            message = "모든 내용을 입력하세요."

        else:
            User.objects.create(username = user_id, password = make_password(password))
            return HttpResponseRedirect(reverse('accountapp:login'))

        return render(request, 'accountapp/create.html', {'message': message})

    def get(self, request):
        return render(request, 'accountapp/create.html')


class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user' # 탬플릿에서 사용하는 user의 객체 이름을 target_user로 다르게 설정해줌
    # 로그인 한 상태에서 자신의 페이지로 들어와 정보를 볼 수 있었지만 이제 다른사람이 그 페이지에 들어가더라도 정상적으로 열람 가능하다.
    template_name = 'accountapp/detail.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(writer=self.get_object()).order_by('-created_at')
        # 현재의 프로젝트에 속한 아티클들만 필터링해서 가져옴
        return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class AccountUpdateView(View):
    model = User
    def post(self, request):
        request_user = self.request.user
        origin_password = request.POST.get('origin-password', None)
        new_password = request.POST.get('password', None)
        re_password = request.POST.get('password2', None)
        if check_password(origin_password, request_user.password):
            if new_password == re_password:
                request_user.set_password(new_password)
                request_user.save()
                return HttpResponseRedirect(reverse('articleapp:list'))
            else:
                message = "새로운 비밀번호를 확인해주세요."
        elif origin_password == None or new_password == None or re_password == None :
            message = "모든 정보를 입력해야 합니다.bin()"
        else:
            message = "현재 사용중인 비밀번호를 확인해주세요."
        return render(request, 'accountapp/update.html', {'message': message})
    def get(self, request):
        return render(request, 'accountapp/update.html')


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'