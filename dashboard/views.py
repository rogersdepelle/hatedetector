from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from .forms import LoginForm, PasswordForm, RecoverPasswordForm, UserForm
from .utils import set_context


def login(request):
    context = set_context(request)
    login_form = LoginForm()
    recover_password_form = RecoverPasswordForm()

    if request.POST:
        if request.POST['form'] == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                request = login_form.save(request=request)
                return redirect('dashboard')
        if request.POST['form'] == 'recover_password':
            recover_password_form = RecoverPasswordForm(request.POST)
            if recover_password_form.is_valid():
                context['notifications'].append(recover_password_form.save())

    context['login_form'] = login_form
    context['recover_password_form'] = recover_password_form

    return render(request, 'login.html', context)


def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(redirect_field_name=None)
def profile(request):
    context = set_context(request)
    password_form = PasswordForm(user=request.user)
    user_form = UserForm(instance=request.user)

    if request.method == 'POST':
        if request.POST['form'] == 'profile':
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                context['notifications'].append(_('Profile updated successfully'))
        if request.POST['form'] == 'password':
            password_form = PasswordForm(request.user, request.POST )
            username = request.user.username
            if password_form.is_valid():
                request = password_form.save(username=username, request=request)
                context['notifications'].append(_('Password updated successfully'))

    context['password_form'] = password_form
    context['user_form'] = user_form

    return render(request, "profile.html", context)
