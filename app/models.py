from django.db import models
from django.contrib.auth.models import User

# Create your models here.

payment_modes = (
    (1,'Citrus'),
    (2,'PayU'),
    (3,'PayPal'),
    (4,'Barclays Card'),
    (5,'Credit Card'),
    (6,'Debit Card'),
    (7,'PayTM'),
    (8,'Google Wallet'),
    (9,'Ola Wallet'),
    (10,'MobiWik'),
    (11,'Oxigen')
)


class MainUser(models.Model):
    name = models.CharField(max_length=300)
    user = models.OneToOneField(User)
    address = models.CharField(max_length=300, null=True, default=None, blank=True) #merchant
    PAN = models.CharField(max_length=400, unique=True)
    billing_address = models.CharField(max_length=400, null=True, default=None,blank=True) #customer
    phone_number = models.CharField(max_length=400)
    email_address = models.CharField(max_length=400)
    shipping_address = models.CharField(max_length=500, null=True, default=None,blank=True) #customer only
    PIN = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=100, decimal_places=5)
    payee_name = models.CharField(max_length=100)
    acc_type = (
        (1,'Merchant'),
        (2,'Customer without PAN'),
        (3,'Customer with PAN')
    )
    type = models.IntegerField(default=1,choices=acc_type)
    gcm = models.CharField(max_length=500)
    merchant_auth = models.CharField(max_length=200)

    class Meta:
        app_label = 'app'

# class Merchant(models.Model):
#     #merch model
#     name = models.CharField(max_length=300)
#     user = models.OneToOneField(User)
#     address = models.CharField(max_length=300)
#     PAN = models.CharField(max_length=400, unique=True)
#
#
# class Customer(models.Model):
#     #customer model
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=100)
#     billing_address = models.CharField(max_length=500)
#     shipping_address = models.CharField(max_length=500)
#     PIN = models.CharField(max_length=4)
#     gcm = models.CharField(max_length=500)

class Prototype(models.Model):
    merchant = models.ForeignKey(MainUser)
    key = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'app'

# class Endpoint(models.Model):
#     # this is the endpoint merchant creates for a transaction
#     PAN = models.CharField(max_length=300)
#     merchant_txn_id = models.CharField(max_length=200)
#     key = models.CharField(max_length=300)
#     created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    prototype = models.ForeignKey(Prototype)
    customer = models.ForeignKey(MainUser)
    choice = (
        (1, 'Successful and Remitted'),
        (2, 'Successful and Not Remitted'),
        (3, 'Failed'),
    )
    status = models.IntegerField(choices=choice)
    mode = models.IntegerField(choices=payment_modes)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'app'

# class Transaction(models.Model):
#     customer = models.ForeignKey(Customer)
#     endpoint = models.ForeignKey(Endpoint)
#     choice = (
#         (1, 'Successful and Remitted'),
#         (2, 'Successful and Not Remitted'),
#         (3, 'Failed'),
#     )
#     status = models.IntegerField(choices=choice)
#     mode = models.IntegerField(choices=payment_modes)
#     created_at = models.DateTimeField(auto_now_add=True)
#     #all products with this transaction are in this invoice


class PersonalTransfer(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.CharField(max_length=500, blank=True, null=True, default=None)
    prototype = models.ForeignKey(Prototype)
    currencies = (
        (1,'INR'),
        (2,'USD'),
        (3,'GBP')
    )
    currency = models.IntegerField(choices=currencies)

    class Meta:
        app_label = 'app'

class Product(models.Model):
    name = models.CharField(max_length=500)
    sku = models.CharField(max_length=500,default=None,null=True,blank=True)
    manufacturer = models.CharField(max_length=500,default=None,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    currencies = (
        (1,'INR'),
        (2,'USD'),
        (3,'GBP')
    )
    quantity = models.IntegerField(default=1,blank=True)
    currency = models.IntegerField(choices=currencies)
    description = models.CharField(max_length=500,default=None,null=True,blank=True)
    prototype = models.ForeignKey(Prototype)

    class Meta:
        app_label = 'app'


# class Balance(models.Model):
#     balance = models.DecimalField(max_digits=20, decimal_places=2)
#     PAN = models.CharField(max_length=500)