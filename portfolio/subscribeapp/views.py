from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views.generic import RedirectView, ListView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from subscribeapp.models import Subscription
from projectapp.models import Project
from articleapp.models import Article
from django.contrib.auth.models import User

@method_decorator(login_required, 'get')
class SubscriptionView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projectapp:detail', kwargs={'pk': self.request.GET.get('project_pk')})

    def get(self, requset, *args, **kwargs):
        project = get_object_or_404(Project, pk = self.request.GET.get('project_pk'))
        # project_pk가진 Project가 없다면 404  오류를 출력해라.
        user = self.request.user

        subscription = Subscription.objects.filter(user=user, project=project)

        if subscription.exists():
            subscription.delete()
        else:
            Subscription(user=user, project=project).save()

        return super(SubscriptionView, self).get(requset, *args, **kwargs)

@method_decorator(login_required, 'get')
class SubscriptionListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'subscribeapp/list.html'
    paginate_by = 20
    # article 전부를 가져오는 것이 아닌 특정 조건(구독여부)를 만족하는 aarticle을 가져올 것
    # 따라서 쿼리셋관련 함수를 새로 작성할 것이다.
    def get_queryset(self):
        projects = Subscription.objects.filter(user=self.request.user).values_list('project')
        # values_list : 값들을 리스트화 시킨다.
        # 따라서 projects에는 구독한모든 프로젝트가 리스트 형식으로 담긴다.
        article_list = Article.objects.filter(project__in=projects).order_by('-created_at')
        return article_list