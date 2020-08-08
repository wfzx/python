from django.db import models

class WebHook(models.Model):
    Address = models.CharField(max_length=256)
    RequestMethod = models.CharField(max_length=8)
    RequestHeader = models.CharField(max_length=200)
    Template = models.CharField(max_length=400)
    Belong = models.CharField(max_length=5)

    def __str__(self):
        return self.Address