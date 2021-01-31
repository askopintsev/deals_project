from django.db import models


class Customer(models.Model):

    customer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.customer)


class Item(models.Model):

    item = models.CharField(max_length=100)

    def __str__(self):
        return str(self.item)


class Deal(models.Model):

    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

