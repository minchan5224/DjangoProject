from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views.generic import RedirectView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from articlelikeapp.models import Articlelike, ArticleUnlike
from django.views import View
import json
from django.http import JsonResponse
from articleapp.models import Article
from django.contrib.auth.models import User
from pytz import timezone
from datetime import datetime

from articlelikeapp import subway_time
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class SubwayTimeView(View):
    template_name = 'articlelikeapp/subway.html'
    def post(self, request):
        content = self.request.body
        content = json.loads(content)
        content = content['userRequest']
        content = content['utterance']
        KST = datetime.now(timezone('Asia/Seoul'))
        dataSend = subway_time.main_service(content, KST)
        return JsonResponse(dataSend)

@method_decorator(login_required, 'get')
class ArticleLikeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': self.request.GET.get('article_pk')})

    def get(self, requset, *args, **kwargs):
        article = get_object_or_404(Article, pk = self.request.GET.get('article_pk'))
        # project_pk가진 Project가 없다면 404  오류를 출력해라.
        user = self.request.user

        articlelike = Articlelike.objects.filter(user=user, article=article)

        if articlelike.exists():
            articlelike.delete() # 좋아요 해제
        else:
            Articlelike(user=user, article=article).save()
            if ArticleUnlike.objects.filter(user=user, article=article).exists():
                ArticleUnlike.objects.filter(user=user, article=article).delete()

        return super(ArticleLikeView, self).get(requset, *args, **kwargs)

@method_decorator(login_required, 'get')
class ArticleUnLikeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': self.request.GET.get('article_pk')})

    def get(self, requset, *args, **kwargs):
        article = get_object_or_404(Article, pk = self.request.GET.get('article_pk'))
        # project_pk가진 Project가 없다면 404  오류를 출력해라.
        user = self.request.user

        articleunlike = ArticleUnlike.objects.filter(user=user, article=article)

        if articleunlike.exists():
            articleunlike.delete()
        else:
            ArticleUnlike(user=user, article=article).save()
            if Articlelike.objects.filter(user=user, article=article).exists():
                Articlelike.objects.filter(user=user, article=article).delete()

        return super(ArticleUnLikeView, self).get(requset, *args, **kwargs)


