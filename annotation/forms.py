from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from comments.models import Comment

from .models import Annotation


class AnnotationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnnotationForm, self).__init__(*args, **kwargs)
        self.fields['kind'].label = ''
        self.fields['other'].label = 'Outro'
        self.fields['is_hate_speech'] = forms.TypedChoiceField( coerce=lambda x: x == 'True', choices=((True, 'Sim'), (False, 'Não')), widget=forms.RadioSelect)
        self.fields['is_hate_speech'].label = ''
        self.fields['is_hate_speech'].required = True

    class Meta:
        model = Annotation
        fields = ('is_hate_speech', 'kind', 'other')
        widgets = {'kind': forms.CheckboxSelectMultiple(),}