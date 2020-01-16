from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from slugify import slugify

from user_profiles.models import UserProfile



RED = 'RD'
BLUE = 'BL'
WATERMELON = 'WM'

SCENE_CHOICES = [
    (RED, 'Красная'),
    (BLUE, 'Синяя'),
    (WATERMELON, 'Арбузик'),
]

class Application(models.Model):
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    GROUP = 'GR'
    SOLO = 'SO'

    FORMAT_CHOICES = [
        (GROUP, 'Группа'),
        (SOLO, 'Сольное выступление'),
    ]

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=30)
    phone = models.CharField(max_length=12, verbose_name='Телефон')

    format = models.CharField(max_length=2, choices=FORMAT_CHOICES, verbose_name='Формат выступления')
    name = models.CharField(max_length=30, verbose_name='Имя группы или исполнителя', unique=True)
    description = models.TextField(verbose_name='Описание')
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='likes', verbose_name='Нравится')
    dislikes = models.ManyToManyField(UserProfile, blank=True, related_name='dislikes', verbose_name='Не нравится')
    abstain = models.ManyToManyField(UserProfile, blank=True, related_name='abstain', verbose_name='Воздерживаюсь')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    accepted = models.BooleanField(default=False, verbose_name='Одобрено')
    denied = models.BooleanField(default=False, verbose_name='Отказано')
    scene = models.CharField(max_length=2, choices=SCENE_CHOICES, verbose_name='Желаемая сцена')

    FRIDAY = 'FR'
    SATURDAY = 'SA'

    DAY_CHOICES = [
        (FRIDAY, 'Пятница'),
        (SATURDAY, 'Суббота'),
    ]

    performance_day = models.CharField(max_length=2, choices=DAY_CHOICES, verbose_name='Желаемый день выступления')
    wishes = models.CharField(max_length=250, blank=True, verbose_name='Пожелания')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('festival_app:view-app-censor', kwargs={'slug': self.slug})


# Автоматическая генерация и установка слагов для заявок.


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = slugify(new_slug)
    qs = Application.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_app_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_app_receiver, sender=Application)


# Автоматический подсчет рейтинга после каждого лайка/дизлайка.
def count_rating(slug):
    app = Application.objects.get(slug=slug)
    app.rating = app.likes.count() - app.dislikes.count()
    app.save()


# Автоматический вердикт для заявки, когда сумма голосов равна количеству цензоров. ( То есть проголосовали
# все цензоры )
def count_votes(slug):
    app = Application.objects.get(slug=slug)
    app_votes = app.likes.count() + app.dislikes.count() + app.abstain.count()
    censors_count = UserProfile.objects.filter(type='CE').count()
    if app_votes == censors_count:
        if app.likes.count() > app.dislikes.count():
            app.accepted = True
            app.save()
        if app.dislikes.count() > app.likes.count():
            app.denied = True
            app.save()
        if app.likes.count() == app.dislikes.count():
            app.denied = True
            app.save()


class Scene(models.Model):

    class Meta:
        verbose_name = 'Сцена'
        verbose_name_plural = 'Сцены'

    title = models.CharField(max_length=2, choices=SCENE_CHOICES, verbose_name='Название сцены')
    description = models.CharField(max_length=300, verbose_name='Описание сцены')
    first_day_afternoon = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 1-ый день днём')
    first_day_evn = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 1-ый день вечером')
    first_day_late_evn = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 1-ый день поздним '
                                                                             'вечером')
    second_day_afternoon = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 2-ой день днём')
    second_day_evn = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 2-ой день вечером')
    second_day_late_evn = models.PositiveIntegerField(default=0, verbose_name='Количество групп в 2-ой день поздним '
                                                                              'вечером')

    def __str__(self):
        return self.title