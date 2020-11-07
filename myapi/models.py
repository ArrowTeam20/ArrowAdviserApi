from django.db import models

# Create your models here.
class LinkItem(models.Model):
    productName = models.CharField(max_length=200)
    linkAmazon = models.URLField()
    linkBeauty = models.URLField()
    def __str__(self):
        return self.productName.__str__()