from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from web_scraping.models import Comment

from .models import Annotation


class AddAnnotationForm(forms.Form):
    User.__str__ = User.get_full_name
    rater = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), empty_label="Selecione Anotador.", label='')
    amount = forms.IntegerField(min_value=1, label='Quantidade')

    def save(self):
        amount = self.cleaned_data['amount']
        rater = self.cleaned_data['rater']
        all_comments = Comment.objects.filter(valid=True)
        all_annotations = Annotation.objects.all()
        comments = []

        for comment in all_comments:
            if not all_annotations.filter(comment=comment, user=rater).exists() and all_annotations.filter(comment=comment).count() < settings.N_RATERS:
                comments.append(comment)
            if len(comments) == amount:
                break

        if len(comments) < amount:
            return 0

        for comment in comments:
            Annotation.objects.create(user=rater, comment=comment)

        return len(comments)


class AnnotationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnnotationForm, self).__init__(*args, **kwargs)
        self.fields['kind'].label = ''
        self.fields['other'].label = 'Outro'
        self.fields['is_hate_speech'] = forms.TypedChoiceField( coerce=lambda x: x == 'True', choices=((True, 'Sim'), (False, 'Não')), widget=forms.RadioSelect)
        self.fields['is_hate_speech'].label = ''

    class Meta:
        model = Annotation
        fields = ('is_hate_speech', 'kind', 'other')
        widgets = {'kind': forms.CheckboxSelectMultiple(),}