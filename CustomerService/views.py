from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from HolidayHousings.models import Comment

@staff_member_required
def manage_comments(request):
    comments = Comment.objects.all()
    return render(request, 'manage_comments.html', {'comments': comments})

@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('manage-comments')

@staff_member_required
def deactivate_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    housing_pk = comment.holiday_housing.pk
    if request.user.is_staff:  # Nur Mitarbeiter können Kommentare deaktivieren
        comment.active = False
        comment.save()
    return redirect('housing-detail', pk=housing_pk)

@staff_member_required
def activate_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    housing_pk = comment.holiday_housing.pk
    if request.user.is_staff:  # Nur Mitarbeiter können Kommentare deaktivieren/aktivieren
        comment.active = not comment.active  # Status umkehren
        comment.save()
    return redirect('housing-detail', pk=housing_pk)
