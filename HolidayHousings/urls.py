from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.housing_list, name='housing-list'),
    path('show/<int:pk>/', views.housing_detail, name='housing-detail'),
    path('add/', views.housing_create, name='housing-create'),
    path('delete/<int:pk>/', views.housing_delete, name='housing-delete'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit-comment'),
    path('vote/<int:pk>/<str:vote_type>/', views.vote, name='vote'),
    path('comment-vote/<int:comment_id>/<str:vote_type>/', views.comment_vote, name='comment-vote')
]
