from django.db import models
from decimal import Decimal
# Create your models here.

class Client_details(models.Model):
    name = models.CharField(max_length=255)
    cif_nif = models.CharField(max_length=50, unique=True)
    direction = models.TextField()
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.name
    

# class Client_Payment(models.Model):
#     Date = pass
#     client_name= models.CharField(max_length=120)
#     Reference = models.name = models.CharField(max_length=length, ${blank=True, null=True})
#     Neto = models.CharField(max_length=100)
#     IVA = models.DecimalField


class add_providers_details(models.Model):
    name = models.CharField(max_length=255)
    cif_cif = models.CharField(max_length=50, unique=True)
    direction = models.TextField()
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    account_number = models.CharField(max_length=150)


    def __str__(self):
        return self.name

class Expense(models.Model):
    date = models.DateField()
    provider = models.ForeignKey(add_providers_details , on_delete=models.CASCADE)
    client = models.ForeignKey(Client_details, on_delete=models.CASCADE)
    bill_no = models.CharField(max_length=120)
    concept = models.CharField(max_length=120)
    neto = models.DecimalField(max_digits=10,decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Expense {self.id} - {self.client.name} ({self.date})"
    

class Funds(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client_details, on_delete=models.CASCADE)
    bill_no = models.CharField(max_length=120)
    concept = models.CharField(max_length=120)
    neto = models.DecimalField(max_digits=10,decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fund {self.id} - {self.client.name} ({self.date})"

    


    