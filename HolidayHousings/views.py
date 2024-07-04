from django.urls import path
# from pyexpat.errors import messages
from django.contrib import messages
from OnlineShop import settings
from . import views, models, forms

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .models import HolidayHousing
from django.shortcuts import render, get_object_or_404, redirect
from .models import HolidayHousing
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import HolidayHousing
from django.shortcuts import render, redirect

from .forms import HolidayHousingForm, CommentForm, EditCommentForm
from .models import Comment, Vote
from .forms import HolidayHousingForm, CommentForm, SearchForm
from django.db.models import Q

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


def clean_max_quantity(self):
    max_quantity = self.cleaned_data.get('max_quantity')
    if max_quantity < 1:
        raise forms.ValidationError("Die maximale Stückanzahl muss mindestens 1 sein.")
    return max_quantity


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
        form = HolidayHousingForm(request.POST, request.FILES)  # request.FILES hinzugefügt
        # form = HolidayHousingForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid():
            housing = form.save(commit=False)
            form.instance.myuser = request.user
            form.save()

            product = Product.objects.create(
                name=housing.title,
                description=housing.specials,
                price=housing.price,
                image=None
            )

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


def housing_search(request):
    if request.method == 'POST':
        search_string_title = request.POST.get('title', '')
        search_string_rooms = request.POST.get('rooms', '')
        search_string_specials = request.POST.get('specials', '')

        print("Title:", search_string_title)
        print("Rooms:", search_string_rooms)
        print("Specials:", search_string_specials)

        # Baue die Abfrage dynamisch auf
        query = Q(title__icontains=search_string_title) & Q(specials__icontains=search_string_specials)

        # Füge die Bedingung für die Zimmeranzahl nur hinzu, wenn ein Wert angegeben wurde
        if search_string_rooms:
            searched_rooms = int(search_string_rooms)
            query &= Q(rooms=searched_rooms)

        housings_found = HolidayHousing.objects.filter(query)

        print("Found housings:", housings_found)

        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': True,
            'form': form_in_function_based_view,
            'housings_found': housings_found
        }
    else:  # GET
        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': False,
            'form': form_in_function_based_view,
        }

    return render(request, 'housing-search.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# def checkout(request):
#  cart_items = CartItem.objects.filter(user=request.user)
# total_price = sum(item.product.price * item.quantity for item in cart_items)
# Fügen Sie hier Ihre Checkout-Logik hinzu
# return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, housing_id):
    housing = get_object_or_404(HolidayHousing, pk=housing_id)
    quantity = int(request.POST.get('quantity', 1))

    # Beispiel: Hier wird angenommen, dass ein Warenkorb in der Sitzung gespeichert wird
    cart = request.session.get('cart', {})
    cart_item = cart.get(housing_id, {'quantity': 0})
    cart_item['quantity'] += quantity
    cart[housing_id] = cart_item
    request.session['cart'] = cart

    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for housing_id, item_data in cart.items():
        housing = get_object_or_404(HolidayHousing, pk=housing_id)
        quantity = item_data['quantity']
        item_total_price = housing.price * quantity
        total_price += item_total_price
        cart_items.append({
            'housing': housing,
            'quantity': quantity,
            'item_total_price': item_total_price,
        })

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []

    # Sammle die Artikel aus dem Warenkorb
    for housing_id, item_data in cart.items():
        housing = get_object_or_404(HolidayHousing, pk=housing_id)
        quantity = item_data['quantity']
        cart_items.append({
            'housing': housing,
            'quantity': quantity,
            'item_total_price': housing.price * quantity,
        })

    # Berechne den Gesamtpreis
    total_price = sum(item['item_total_price'] for item in cart_items)

    if request.method == 'POST':
        # Beispiel: Hier könnte die Bezahllogik oder Bestellverarbeitung stattfinden
        # Für dieses Beispiel wird der Warenkorb nach dem Checkout geleert
        request.session['cart'] = {}

        # Erstellen einer Bestellungsbestätigung oder Weiterleitung zu einer Bestätigungsseite
        return redirect('order_confirmation')  # Anpassen zu Ihrer Bestätigungsseite

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
