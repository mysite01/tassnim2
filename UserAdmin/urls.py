from django.urls import path
# from UserAdmin.views import SignUpView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #  path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MySignUpView.as_view(), name='signup'),
    path('show_myusers/', views.MyUserListView.as_view(), name='myuser-list'),
]

