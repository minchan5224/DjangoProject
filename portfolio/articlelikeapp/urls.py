from django.urls import path
from articlelikeapp.views import ArticleLikeView, ArticleUnLikeView, SubwayTimeView
app_name = 'articlelikeapp'

urlpatterns = [
    path('like/', ArticleLikeView.as_view(), name='like'),
    path('unlike/', ArticleUnLikeView.as_view(), name='unlike'),
    path('subway/', SubwayTimeView.as_view(), name='subway'),
]