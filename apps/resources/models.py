from django.db import models

class Resource(models.Model):
    resource_types = (
        ('image', 'Image'),
        ('audio', 'Audio')
    )
    resource_type = models.CharField(max_length=255, choices=resource_types)
    user = models.ForeignKey('accounts.OpenspritesUser')