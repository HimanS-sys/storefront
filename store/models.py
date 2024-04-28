from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length = 255)
    featured_product = models.ForeignKey(
        "Product",
        on_delete = models.SET_NULL,
        null = True,
        related_name = "+",
    )

class Product(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(
        null = True,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    collection = models.ForeignKey(
        Collection,
        on_delete = models.PROTECT,
    )

    promotions = models.ManyToManyField(
        Promotion,
        related_name = "products",
    )

class Customer(models.Model):
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, "Gold"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_BRONZE, "Bronze"),
    ]
    givenname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 255)
    birth_date = models.DateTimeField(null = True)
    membership = models.CharField(
        max_length = 1,
        choices = MEMBERSHIP_CHOICES,
        default = MEMBERSHIP_BRONZE,
    )

    class Meta:
        indexes = [
            models.Index(fields = ["lastname", "givenname"])
        ] 

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add = True)
    PAYMENT_STATUS_DONE = "C"
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_DONE, "Complete"),
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    payment_status = models.CharField(
        max_length = 1,
        choices = PAYMENT_STATUS_CHOICES,
        default = PAYMENT_STATUS_PENDING,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete = models.PROTECT,
    ) 

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete = models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT,
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
    )

class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    customer = models.ForeignKey(
        Customer,
        on_delete = models.CASCADE,
    )
    zip = models.CharField(max_length = 255, null = True) # Change it to proper field, refer docs for field types

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete = models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField()