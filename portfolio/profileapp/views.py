from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, UpdateView

from profileapp.forms import ProfileCreationForm
from profileapp.models import Profile

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from profileapp.decorators import profile_ownership_required
# ^ 데코레이터 import


class ProfileCreateView(CreateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreationForm
    template_name = 'profileapp/create.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        # 임시로 저장할것이다. commit=False를 통해 임시 저장용도로 사용이 가능하다.
        # 지금은 form에서 받은 값.('image', 'nickname', 'message')만 있다
        temp_profile.user = self.request.user
        # user도 필요하기때문에 로그인한 사람의 profile만 수정 가능하도록 request를 보낸 사람의 user을 합쳐준다
        temp_profile.save()
        # 필요한 정보가 완성 되었으니 저장한다.
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.user.pk})
        # reverse 혹은 reverse_lazy 둘다 사용 가능하다.
        # self.object 는 Profile를 가리킨다. 그 Profile의 user의 pk를 찾아 넘겨주는것.

@method_decorator(profile_ownership_required, 'get')
@method_decorator(profile_ownership_required, 'post')
class ProfileUpdateView(UpdateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('accountapp:home')
    template_name = 'profileapp/update.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        # 임시로 저장할것이다. commit=False를 통해 임시 저장용도로 사용이 가능하다.
        # 지금은 form에서 받은 값.('image', 'nickname', 'message')만 있다
        temp_profile.user = self.request.user
        # user도 필요하기때문에 로그인한 사람의 profile만 수정 가능하도록 request를 보낸 사람의 user을 합쳐준다
        temp_profile.save()
        # 필요한 정보가 완성 되었으니 저장한다.
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.user.pk})
        # reverse 혹은 reverse_lazy 둘다 사용 가능하다.
        # self.object 는 Profile를 가리킨다. 그 Profile의 user의 pk를 찾아 넘겨주는것.