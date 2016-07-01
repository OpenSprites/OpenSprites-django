from django.db import models

def upload_resource_path(instance, filename):
    return '{0}_{1}'.format(instance.user.id, filename)

class Resource(models.Model):
    resource_types = (
        ('image', 'Image'),
        ('audio', 'Audio')
    )
    resource_type = models.CharField(max_length=255, choices=resource_types)
    user = models.ForeignKey('accounts.OpenspritesUser')
    file = models.FileField(upload_to=upload_resource_path)