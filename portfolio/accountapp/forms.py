from django.contrib.auth.forms import UserCreationForm

class AccountUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True
        # 위의 코드가 없다면 AccountUpdateForm와 UserCreationForm 가 같다.
        # 하지만 위의 코드가 있다면 초기화 이후 'username'의 값을 비활성시킨다.
        # 또한 누군가가 임의로 값을 바꾸어 보내더라도 비활성화 되어있기 때문에 서버에 적용되지 않는다.