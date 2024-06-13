from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import MySignUpForm
from .models import MyUser
# Create your views here.
# UserAdmin/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# class SignUpView(generic.CreateView):
#   form_class = UserCreationForm
# success_url = reverse_lazy('login')
# template_name = 'registration/signup.html'


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """
        At this point the security check complete.
        The user gets logged in here the user in
        and custom code gets performed.
        """
        auth_login(self.request, form.get_user())
        form.get_user().execute_after_login()  # custom code

        return HttpResponseRedirect(self.get_success_url())


class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser-list.html'

    def get_context_data(self, **kwargs):
        context = super(MyUserListView, self).get_context_data(**kwargs)
        print(context["object_list"][0])
        return context


class HomeBirthdayView(TemplateView):

    def get_context_data(self, **kwargs):
        myuser = self.request.user  # Class is MyUser, not User
        # print('CHECKING (My)User class: ', myuser.__class__.__name__)

        myuser_has_birthday_today = myuser.is_authenticated and myuser.has_birthday_today()

        context = super(HomeBirthdayView, self).get_context_data(**kwargs)
        context['myuser_has_birthday_today'] = myuser_has_birthday_today

        return context
