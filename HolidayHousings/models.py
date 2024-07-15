from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# from UserAdmin.models import MyUser
from UserAdmin.models import MyUser


class HolidayHousing(models.Model):
    TYPE = [
        ('F', 'flat'),
        ('H', 'house'),
        ('S', 'special location')
    ]

    type = models.CharField(
        max_length=1,
        choices=TYPE
    )

    COSTS = [
        ('C', 'cheap'),
        ('A', 'affordable'),
        ('E', 'expensive'),
        ('L', 'luxury')
    ]

    costs = models.CharField(
        max_length=1,
        choices=COSTS
    )

    LOCATION = [
        ('M', 'metropolis'),
        ('V', 'village'),
        ('N', 'nature'),
        ('C', 'city')
    ]

    location = models.CharField(
        max_length=1,
        choices=LOCATION
    )

    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='housing_images/', null=True, blank=True)  # ImageField hinzugefügt
    rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField für den Preis hinzugefügt

    def __str__(self):
        return f'{self.title} - {self.price} €'

    max_quantity = models.PositiveIntegerField(default=1, help_text='Maximale Stückanzahl pro Bestellung')
    specials = models.CharField(max_length=50)
    image = models.ImageField(upload_to='holiday_housing_images/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='holiday_housing_pdfs/', blank=True, null=True)
    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='holiday_housing_created_by',
        related_query_name='holiday_housing_created_by'
    )

    # image = models.ImageField(upload_to='housing_images/', null=True, blank=True)  # ImageField hinzugefügt

    def get_total_cart_quantity(self):
        # Beispiel: Anzahl der Holiday Housings im Warenkorb
        return self.cart_items.count()  # Annahme: Verknüpfung mit einem Warenkorbelement-Modell

    def get_total_cart_price(self):
        # Beispiel: Gesamtpreis der Holiday Housings im Warenkorb
        return self.cart_items.count() * self.price  # Annahme: Verknüpfung mit einem Warenkorbelement-Modell

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U', holiday_housing=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D', holiday_housing=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, myuser, up_or_down):
        possible_votes = {
            'up': 'U',
            'down': 'D'
        }

        users_vote = possible_votes.get(up_or_down)

        if users_vote is not None:
            Vote.objects.create(
                up_or_down=users_vote,
                myuser=myuser,
                holiday_housing=self
            )
        else:
            print('Invalid Vote value!! : ', up_or_down)

    class Meta:
        ordering = ['costs', 'type', 'location']
        verbose_name = 'Holiday Housing'
        verbose_name_plural = 'Holiday Housings'

    def __str__(self):
        def get_str_for_rooms():
            if self.rooms > 1:
                return 'rooms'
            return 'room'

        return f'{self.title} - {self.get_costs_display()} {self.rooms} {get_str_for_rooms()} {self.get_type_display()} in {self.get_location_display()}'

    def __repr__(self):
        return f'{self.title} / Location: {self.get_location_display()} / Costs: {self.get_costs_display()} / Type: {self.get_type_display()} / Rooms: {self.rooms} / Specials: {self.specials}'


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1, choices=VOTE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    holiday_housing = models.ForeignKey(HolidayHousing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.up_or_down} on {self.holiday_housing} by {self.myuser.username}'

    def __repr__(self):
        return f'{self.up_or_down} on {self.holiday_housing} by {self.myuser.username} ({self.timestamp})'


class Comment(models.Model):
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    holiday_housing = models.ForeignKey(HolidayHousing, on_delete=models.CASCADE)
    star_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    active = models.BooleanField(default=True)

    def get_helpful_count(self):
        return CommentVote.objects.filter(comment=self, vote_type='U').count()

    def get_not_helpful_count(self):
        return CommentVote.objects.filter(comment=self, vote_type='D').count()

    class Meta:
        unique_together = ('myuser', 'holiday_housing')  # Ensure one comment per user per housing

        def __str__(self):
            return f'{self.get_comment_excerpt()} ({self.myuser.username})'

        def __repr__(self):
            return f'{self.get_comment_excerpt()} ({self.myuser.username} / {str(self.timestamp)})'

    def get_comment_excerpt(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text

    def __str__(self):
        return f'{self.get_comment_excerpt()} ({self.myuser.username})'

    def __repr__(self):
        return f'{self.get_comment_excerpt()} ({self.myuser.username} / {str(self.timestamp)})'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

# class CartItem(models.Model):
#   product = models.ForeignKey(Product, on_delete=models.CASCADE)
# quantity = models.PositiveIntegerField(default=1)
# user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# date_added = models.DateTimeField(auto_now_add=True)

# def __str__(self):
#   return f'{self.quantity} x {self.product.name}'

# user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    housing = models.ForeignKey('HolidayHousing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.housing.title} in Order #{self.order.id}'

class CommentVote(models.Model):
    VOTE_TYPES = [('U', 'Helpful'), ('D', 'Not Helpful')]
    vote_type = models.CharField(max_length=1, choices=VOTE_TYPES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vote_type} on {self.comment} by {self.user.username}'

    def __repr__(self):
        return f'{self.vote_type} on {self.comment} by {self.user.username}'

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report on {self.comment} by {self.user.username}'

    def __repr__(self):
        return f'Report on {self.comment} by {self.user.username} ({self.timestamp})'