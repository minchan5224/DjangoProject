from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from articleapp.forms import ArticleCreationForm
from articleapp.models import Article
from articlelikeapp.models import Articlelike, ArticleUnlike

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articleapp.decorators import article_ownership_required
from django.utils import timezone

from commentapp.forms import CommentCreationForm
from django.views.generic.edit import FormMixin

from projectapp.models import Project


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/create.html'

    def form_valid(self, form):
        # if self.request.user.is_superuser:
        temp_article = form.save(commit=False) # 임시저장
        temp_article.writer = self.request.user # 지금 리퀘스트를 보낸 사람을 writer로 저장
        temp_article.created_at = timezone.localtime()
        temp_article.save() #저장
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})

class ArticleDetailView(DetailView, FormMixin): # FormMixin을 이용해 다중 상속을 받는다
    model = Article
    form_class = CommentCreationForm
    # 필요한 form을 가져온다.
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'

    def get_context_data(self, **kwargs):
        article = self.object
        user = self.request.user
        # comment = Comment.objects.filter(article=article)
        # commentlike = []
        # commentunlike =[]
        print(article, user)
        if user.is_authenticated: # 유저가 로그인 중이라면
            articlelike = Articlelike.objects.filter(user=user, article=article)
            articleunlike = ArticleUnlike.objects.filter(user=user, article=article)
        else:
            articlelike = Articlelike.objects.filter(article=article)
            articleunlike = ArticleUnlike.objects.filter(article=article)
            # for i in comment:
            #     commentlike.append(Commentlike.objects.filter(user=user, article=article, comment=i))
            #     commentunlike.append(CommentUnlike.objects.filter(user=user, article=article, comment=i))
        # 현재의 프로젝트에 속한 아티클들만 필터링해서 가져옴
        # return super(ArticleDetailView, self).get_context_data(articlelike=articlelike, articleunlike=articleunlike, commentlike=commentlike, commentunlike=commentunlike, **kwargs)
        return super(ArticleDetailView, self).get_context_data(articlelike=articlelike, articleunlike=articleunlike, **kwargs)


@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/update.html'
    context_object_name = 'target_article'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html'

class ArticleListView(ListView):
    Article.objects.all().order_by('created_at')
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 50
    # 하나의 페이지에 몇개의 객체를 보여줄 것인지
    # Pagination을 하면 page_obj를 사용할 수 있다.
    def get_queryset(self):
        article_list = Article.objects.all().order_by('-created_at')
        # values_list : 값들을 리스트화 시킨다.
        # 따라서 projects에는 구독한모든 프로젝트가 리스트 형식으로 담긴다.
        return article_list