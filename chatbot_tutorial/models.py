from django.db import models

"""model for saving the counts of requests"""
class RequestCounts(models.Model):
    username = models.CharField(max_length = 30)
    stupid = models.IntegerField()
    fat = models.IntegerField()
    dump = models.IntegerField()
