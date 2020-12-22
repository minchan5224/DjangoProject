from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from recommentapp.forms import RecommentCreationForm
from recommentapp.models import Recomment
from commentapp.models import Comment
from articleapp.models import Article

from recommentapp.decorators import Recomment_ownership_required
from django.utils.decorators import method_decorator


class RecommentCreateView(CreateView):
    model = Recomment
    form_class = RecommentCreationForm
    template_name = 'recommentapp/create.html'

    def form_valid(self, form):
        temp_comment = form.save(commit=False) #임시 저장
        temp_comment.comment = Comment.objects.get(pk=self.request.POST['comment_pk'])
        temp_comment.article = Article.objects.get(pk=self.request.POST['article_pk'])
        # 리퀘스트에서 받은 post데이터중 comment_pk 데이터를 comment 설정해주는것
        # 즉 create.html에서 hidden으로 보낸 comment.pk가 이쪽으로 넘어 오는것
        temp_comment.writer = self.request.user
        temp_comment.save() # 최종적으로 저장
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})
        # object(comment)의 article의 pk를 가진 detail로 되돌아 가는것.

@method_decorator(Recomment_ownership_required, 'get')
@method_decorator(Recomment_ownership_required, 'post')
class RecommentDeleteView(DeleteView):
    model = Recomment
    context_object_name = 'target_comment'
    template_name = 'recommentapp/delete.html'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.request.POST['article_pk']})