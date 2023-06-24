from __future__ import annotations
import datetime
import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from store.interaction import Status
import store.interaction as db

class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)

    def __str__(self):
        return self.address


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=254, unique=True)
    phoneNumber = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256) # DON'T STORE AS PLAIN TEXT
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)

    def getPurchaseHistory(self) -> list:
        return [oi.item for oi in
            OrderItem.objects.
                filter(Q(order__customer=self) & Q(order__status=Order.OrderStatus.COMPLETED)).
                order_by("-quantity").all()]

    def getByUserName(username: str) -> Customer | None:
        return Customer.objects.filter(username=username).first()

    def createCart(self, address: ShippingAddress=None) -> Order:
        if address == None:
            address = self.address
        return Order.objects.create(customer=self, address=address)

    # if nothing is added to the cart, then it's None
    def getCart(self) -> Order | None:
        return Order.objects.filter(Q(status=Order.OrderStatus.CART) & Q(customer=self)).first()

    def chooseItem(itemType) -> Item | None:
        return Item.objects.filter(Q(type=itemType) & Q(status=Item.OrderStatus.STORAGE)).first()

    def addItemToCart(self, itemType) -> tuple[Status, str]:
        item = Customer.chooseItem(itemType)
        if item == None:
            return (Status.FAILURE, "Out of stock")
        item.status = Item.OrderStatus.ON_HOLD
        item.save()

        cart = self.getCart()
        if cart == None:
            cart = self.createCart()
        
        OrderItem.objects.create(order=cart, item=item)
        return (Status.SUCCESS, "")

    def removeItemFromCart(self, itemType) -> tuple[Status, str]:
        cart = self.getCart()
        orderItem = OrderItem.objects.filter(Q(order=cart) & Q(item__type=itemType)).first()
        if orderItem != None:
            orderItem.item.status = Item.OrderStatus.STORAGE
            orderItem.item.save()
            orderItem.delete()
            if OrderItem.objects.filter(order=cart).count() == 0:
                cart.delete()
            return (Status.SUCCESS, "")
        else:
            return (Status.FAILURE, "Cart doesn't have " + str(itemType))

    def shipOrder(self):
        cart = self.getCart()
        if cart != None:
            cart.complete()
            return Status.SUCCESS
        else:
            return Status.FAILURE

    def linkCustomerAddress(self, address: ShippingAddress):
        self.address = address
        self.save()

    def __str__(self):
        return self.name


class QualityType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Quality(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(QualityType, on_delete=models.CASCADE)
    value = models.DecimalField(default=0.0, decimal_places=5, max_digits=6, validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])

    def __str__(self):
        return str(self.type) + '=' + str(self.value)


class ItemCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=64)
    # image link
    logoImage = models.CharField(max_length=300, default="https://www.clipartmax.com/png/full/260-2603496_perfume-bottle-outline-free-icon-perfume-bottle-outline.png")

    def __str__(self):
        return self.name


class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    priceCents = models.IntegerField() # in USD cents
    salePrice = models.IntegerField() # if == price/null: no sale
    sizeOz = models.FloatField() # in oz.

    class Gender(models.TextChoices):
        MALE = 'M',
        FEMALE = 'F',
        UNISEX = 'X',
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices
    )
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=300) # image link

    @property
    def quantity(self) -> int:
        return Item.objects.filter(Q(type=self) & Q(status=Item.OrderStatus.STORAGE)).count()

    def __str__(self):
        return self.name


class BestSellers(models.Model):
    id = models.AutoField(primary_key=True)
    itemType = models.OneToOneField(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.itemType)


class NewArrivals(models.Model):
    id = models.AutoField(primary_key=True)
    itemType = models.OneToOneField(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.itemType)


class QualityItemTypeJoin(models.Model):
    id = models.AutoField(primary_key=True)
    quality = models.OneToOneField(Quality, on_delete=models.CASCADE)
    itemType = models.ForeignKey(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality) + ' ' + str(self.itemType)


class QualityCustomerJoin(models.Model):
    id = models.AutoField(primary_key=True)
    quality = models.OneToOneField(Quality, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality) + ' ' + str(self.customer)


class Item(models.Model): # corresponds to one physical existing item
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    creationDate = models.DateField(null=True)
    class OrderStatus(models.TextChoices):
        STORAGE = 'st',
        ON_HOLD = 'oh',
        SOLD = 'so',
    status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices
    )
    soldDate = models.DateField(null=True) # NULL = unsold
    manufacturerID = models.CharField(max_length=50)

    def make(type) -> Item:
        Item.objects.create(type=type, creationDate=datetime.date.today(), status=Item.OrderStatus.STORAGE, manufacturerID=uuid.uuid4())

    def __str__(self):
        return str(self.type) + ' ' + self.manufacturerID


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(ShippingAddress, null=True, on_delete=models.CASCADE)

    class OrderStatus(models.TextChoices):
        CART = 'ca',
    #   SHIPPED = 'sh',
        COMPLETED = 'co',
    #   CANCELLED = 'xx',
    status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.CART
    )

    def complete(self):
        self.status = Order.OrderStatus.COMPLETED
        for orderItem in OrderItem.objects.filter(order=self):
            orderItem.item.status = Item.OrderStatus.SOLD
            orderItem.delete()
            orderItem.item.save() # doing this after avoids rare database misalign

    def __str__(self):
        return "Order for " + self.customer.name


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)

    def __str__(self):
        return "Order " + str(self.item)

