from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import (FormView, UpdateView, CreateView,
                                       DeleteView)

from .forms import LoginForm, JoinForm
from .models import OpenspritesUser

class Join(FormView):
    template_name = 'register.html'
    form_class = JoinForm
    success_url = '/'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('index'))
        return super(Join, self).get(request)

    def form_valid(self, form):
        super(Join, self).form_valid(form)
        form.save()
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        user.set_ip(self.request)
        return redirect(reverse('index'))

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
                # else:
                #     return redirect(reverse('ban-page'))
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
    def get(self, request, user):
        try:
            user = request.user if user == '' else OpenspritesUser.objects.get(username__iexact=user)
            username = user.username
        except request.user.DoesNotExist:
            username = user
            user = None
        return render(request, self.template_name, {'user': user, 'username': username,})