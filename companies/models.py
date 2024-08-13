from django.db import models


class Enterprise(models.Model):
    name = models.CharField(max_length=175)
    owner = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE)
    
class Employee(models.Model):
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    enterprise = models.ForeignKey(to=Enterprise, on_delete=models.CASCADE)
