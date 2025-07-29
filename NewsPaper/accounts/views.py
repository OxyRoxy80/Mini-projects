from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import CustomSignupForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


class CustomSignupForm(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/'

@login_required
def upgrade_me(request):
    author_group = Group.objects.get(name='authors')
    if request.user not in author_group.user_set.all():
        author_group.user_set.add(request.user)
        messages.success(request, 'Поздравляем! Теперь вы автор!')
    return redirect('profile')

@login_required
def profile_view(request):
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request, 'account/profile.html', {'is_author': is_author})