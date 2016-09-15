from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count

from web_scraping.models import Comment

from .models import Annotation


class AddAnnotationForm(forms.Form):
    rater = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Selecione Anotador.", label='')
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
        
        for comment in comments:
            Annotation.objects.create(user=rater, comment=comment)

        return len(comments)


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation  
        fields = ('is_hate_speech', 'kind')
    