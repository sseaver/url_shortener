from django.shortcuts import render
from app.models import Bookmark, Click
from django.contrib.auth.models import User
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView
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
    fields = ('title', 'description', 'link', 'public')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.random_id = get_random_string(length=6)
        return super().form_valid(form)


class BookmarkView(DetailView):
    model = Bookmark


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    success_url = "/"
    fields = ("title", "description", "link", 'public')


class PrivateBookmarkView(ListView):
    template_name = "private_bookmarks.html"
    model = Bookmark


def link_view(request, short_url):
    reroute = Bookmark.objects.get(random_id=short_url)
    Click.objects.create(bookmark=reroute)
    return HttpResponseRedirect(reroute.link)


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"
