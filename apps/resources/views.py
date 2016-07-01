from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.edit import (FormView, UpdateView, CreateView,
                                       DeleteView)

from .forms import ResourceUploadForm

class ResourceUploadView(CreateView):
    form_class = ResourceUploadView
    template_name = 'share.html'