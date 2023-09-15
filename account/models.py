from django.db import models
from django.conf import settings
from filer.fields.image import FilerImageField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=12)
    photo = models.ImageField(null=True, blank=True,
                              verbose_name='Фото')

    def __str__(self):
        return f'Profile of {self.user.username}'