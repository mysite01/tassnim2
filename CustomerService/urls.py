from django.urls import path
from .views import manage_comments, delete_comment, deactivate_comment, activate_comment

urlpatterns = [
    path('manage-comments/', manage_comments, name='manage-comments'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),
    path('deactivate-comment/<int:comment_id>/', deactivate_comment, name='deactivate-comment'),
    path('activate-comment/<int:comment_id>/', activate_comment, name='activate-comment')
]