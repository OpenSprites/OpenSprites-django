import string
import random

from pyquery import PyQuery as pq

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View
from django.views.generic.edit import (FormView, UpdateView, CreateView,
                                       DeleteView)

from apps.core.utils import get_or_none
from .forms import LoginForm, JoinForm
from .models import OpenspritesUser

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# TODO: MAKE POST REQUEST
class Logoff(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class Join(FormView):
    template_name = 'register.html'
    form_class = JoinForm
    success_url = '/'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('index'))
        request.session['confirmation_id'] = id_generator()
        return super(Join, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(Join, self).get_context_data(**kwargs)
        context['confirmation_id'] = self.request.session.get('confirmation_id', '')
        return context

    def form_valid(self, form):
        confirmation_id = self.request.session.get('confirmation_id', '')
        super(Join, self).form_valid(form)
        doc = pq(url='https://scratch.mit.edu/site-api/comments/project/107940884/')
        found = len(doc('[data-comment-user="{0}"] + div .content:contains("{1}")'.format('Firedrake969', 'test')))
        if found != 0 and confirmation_id != '':
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            login(self.request, user)
            del self.request.session['confirmation_id']
            return redirect(reverse('index'))
        else:
            form.errors['non_field_errors'] = ['Code not found!']
            return render(self.request, 'register.html',
                          {'form': form})
            

class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('index'))
        return super(Login, self).get(request)
    
    def form_valid(self, form):
        super(Login, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                if not user.banned:
                    return super(Login, self).form_valid(form)
            else:
                form.errors['non_field_errors'] = ['Your account is not active.']
                return render(self.request, 'index.html',
                              {'form': form})
        else:
            form.errors['non_field_errors'] = ['Invalid login']
            return render(self.request, 'login.html',
                          {'form': form})


class AccountPage(TemplateView):
    template_name = 'account.html'

    def get(self, request, **kwargs):
        if not kwargs.get('user') and not request.user.is_authenticated:
            return redirect('/')
        return super(AccountPage, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AccountPage, self).get_context_data(**kwargs)
        if not self.kwargs.get('user'):
            context['user'] = self.request.user
            context['username'] = self.request.user.username
        else:
            context['user'] = get_or_none(OpenspritesUser, username__iexact=self.kwargs['user'])
            context['username'] = self.kwargs['user']
        return context
