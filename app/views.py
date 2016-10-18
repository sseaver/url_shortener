from django.shortcuts import render
from app.models import Bookmark, Click
from django.contrib.auth.models import User
from django.views.generic import View, ListView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string


# Create your views here.


class IndexView(ListView):
    template_name = "index.html"
    model = Bookmark


class BookmarkCreateView(CreateView):
    model = Bookmark
    success_url = "/"
    fields = ('title', 'description', 'link')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.random_id = get_random_string(length=6)
        return super().form_valid(form)


class BookmarkView(DetailView):
    model = Bookmark


def link_view(request, short_url):
    reroute = Bookmark.objects.get(random_id=short_url)
    Click.objects.create(bookmark=reroute)
    return HttpResponseRedirect(reroute.link)


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"


class ClickView(CreateView):
    model = Click
    success_url = "/"
    fields = ("clicked",)

    def form_valid(self, form):
        Click.objects.get(bookmark=self.request.bookmark)
        instance = form.save(commit=False)
        instance.bookmark = Bookmark.objects.get(pk=self.kwargs["pk"])
