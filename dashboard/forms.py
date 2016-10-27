from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_password(self):
        try:
            username = User.objects.get(email=self.cleaned_data['email'])
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    return password
                else:
                    raise ValidationError(_("Your system access has been temporarily disabled"))
            else:
                raise ValidationError(_("Email and/or password are invalid"))
        except:
            raise ValidationError(_("Email and/or password are invalid"))

    def save(self, request):
        user = User.objects.get(email=self.cleaned_data['email'])
        login(request, user)
        return request


class PasswordForm(PasswordChangeForm):

    def save(self, username, request, commit=True):
        password_form = super(PasswordForm, self).save(commit=False)
        password = self.cleaned_data['new_password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        if commit:
            password_form.save()
        return request


class RecoverPasswordForm(forms.Form):
    email_recover = forms.EmailField(required=True)

    def save(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email_recover'])
            password = User.objects.make_random_password()
            user.set_password(password)
            message = _("New password: " + password + ". Which will be able to be changed in the next access.")
            error_message = _("The password recovery system is temporarily unavailable, please try again later.")
            try:
                if 1 == send_mail("Password Recovery", message, settings.EMAIL_HOST_USER, [self.cleaned_data['email_recover']], fail_silently=False):
                    user.save()
                    return _("It sent an email with a new password.")
                else:
                    return error_message
            except:
                return error_message
        except:
            return _("Invalid email.")


 
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
