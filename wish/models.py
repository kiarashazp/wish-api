from django.db import models
from accounts.models import User


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fulfilled = models.BooleanField(default=False)
    slug = models.SlugField(auto_created=True)

    class Meta:
        verbose_name = 'wish'
        verbose_name_plural = 'wishes'

    def __str__(self):
        return f'{self.user} <-> {self.title[:20]}'
