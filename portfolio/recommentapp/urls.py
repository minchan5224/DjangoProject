from django.urls import path
from recommentapp.views import RecommentCreateView, RecommentDeleteView
app_name = 'recommentapp'

urlpatterns = [
    path('create/', RecommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>', RecommentDeleteView.as_view(), name='delete'),
]