from django.urls import path
from accountapp.views import AccountCreateView, AccountDetailView, AccountUpdateView, AccountDeleteView
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'accountapp'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accountapp/login.html'), name='login'),
    # LoginView 같은 경우는 템플릿을 지정해줘야 한다.(직접 만들것임.)
    path('logout/', LogoutView.as_view(), name='logout'),
    # LoginView와 LogoutView 둘다 import 필요.

    path('create/', AccountCreateView.as_view(), name='create'),

    path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
    path('update/', AccountUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete')
]