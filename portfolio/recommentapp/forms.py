from django.forms import ModelForm
from recommentapp.models import Recomment

class RecommentCreationForm(ModelForm):
    class Meta:
        model = Recomment
        fields = ['content']