from django.db import models




class OrderItem(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="order")
    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
