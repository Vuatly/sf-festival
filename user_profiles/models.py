from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Пользовательский профиль'
        verbose_name_plural = 'Пользовательские профили'

    MUSICAN = 'MU'
    CENSOR = 'CE'
    ADMIN = 'AD'

    USER_TYPE_CHOICES = [
        (MUSICAN, 'Музыкант'),
        (CENSOR, 'Цензор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, verbose_name='Тип пользователя', default=MUSICAN)

    def __str__(self):
        return self.user.username


# Автоматическое создание профиля, после регистрации.

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


