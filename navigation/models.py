from django.db import models
class Store(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    category = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name 