from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from comments.models import Comment

from .models import Annotation, Annotator


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


    def save(self, annotator, comment, commit=True):
        instance = super(AnnotationForm, self).save(commit=False)
        instance.annotator = annotator
        instance.comment = comment
        if commit:
            instance.save()
        self.save_m2m()
        return instance



class AnnotatorForm(forms.ModelForm):

    class Meta:
        model = Annotator
        fields = ('email',)
