from django.db import models

from base.models import AbstractBaseAppModel

class Talent(AbstractBaseAppModel):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True, null=True)
    source = models.CharField(max_length=128, default='LinkedIN')
    reference_id = models.CharField(max_length=256, unique=True)

    class Meta:
        db_table = 't_talent'
        verbose_name = 'Talent'
        verbose_name_plural = 'Talents'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'


