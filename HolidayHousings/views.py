from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import HolidayHousing
from .forms import HolidayHousingForm, CommentForm, EditCommentForm
from .models import Comment, Vote

from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import HolidayHousing, Comment
from .forms import HolidayHousingForm, CommentForm
# from UserAdmin.models import get_myuser_from_user
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import HolidayHousing, Comment
from .forms import HolidayHousingForm, CommentForm


def housing_list(request):
    all_housings = HolidayHousing.objects.all()
    comments = Comment.objects.all()
    return render(request, 'housing-list.html', {'all_housings': all_housings, 'comments': comments})


def vote(request, pk: str, up_or_down: str):
    myuser = request.user

    holiday_housing = HolidayHousing.objects.get(id=int(pk))

    holiday_housing.vote(myuser, up_or_down)

    return redirect('housing-detail', pk=pk)


def housing_detail(request, pk):
    current_single_housing = get_object_or_404(HolidayHousing, pk=pk)
    current_myuser = request.user

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.myuser = current_myuser
        comment_form.instance.holiday_housing = current_single_housing
        if comment_form.is_valid():
            comment_form.save()
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(holiday_housing=current_single_housing)

    context = {
        'single_housing': current_single_housing,
        'comments_on_the_housing': comments,
        'upvotes': current_single_housing.get_upvotes_count(),
        'downvotes': current_single_housing.get_downvotes_count(),
        'comment_form': comment_form,
    }

    return render(request, 'housing-detail.html', context)


def housing_create(request):
    if request.method == 'POST':
        form = HolidayHousingForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid():
            housing = form.save(commit=False)
            form.instance.myuser = request.user
            form.save()

            comment = comment_form.save(commit=False)
            comment.myuser = request.user
            comment.holiday_housing = housing
            comment.save()

            return redirect('housing-list')
    else:
        form = HolidayHousingForm()
        comment_form = CommentForm()
    return render(request, 'housing-create.html', {'form': form, 'comment_form': comment_form})


def housing_delete(request, pk):
    housing = get_object_or_404(HolidayHousing, pk=pk)
    if request.method == 'POST':
        housing.delete()
        return redirect('housing-list')
    return render(request, 'housing-delete.html', {'housing': housing})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('housing-detail', pk=comment.housing.pk)

    if request.method == 'POST':
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('housing-detail', pk=comment.housing.pk)
    else:
        form = EditCommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    housing_pk = comment.housing.pk
    comment.delete()
    return redirect('housing-detail', pk=housing_pk)


def comment_vote(request, comment_id, vote_type):
    user = request.user
    comment = get_object_or_404(Comment, id=comment_id)

    # Überprüfen, ob der Benutzer bereits für diesen Kommentar abgestimmt hat
    existing_vote = Vote.objects.filter(user=user, holiday_housing=comment.holiday_housing).first()
    if existing_vote:
        existing_vote.delete()

    # Neue Stimme hinzufügen
    Vote.objects.create(user=user, holiday_housing=comment.holiday_housing, up_or_down=vote_type)

    return redirect('housing-detail', pk=comment.holiday_housing.pk)


# ich konnte leider nicht sehen ob ich schon ein upvote oder downvote gegeben habe, auf der detail Seite

class HousingCreateView(CreateView):
    model = HolidayHousing
    form_class = HolidayHousingForm
    template_name = 'housing-create.html'
    success_url = reverse_lazy('housing-list')

    def form_valid(self, form):
        # myuser = get_myuser_from_user(self.request.user)

        # if myuser is not None:
        form.instance.myuser = self.request.user

        return super().form_valid(form)
