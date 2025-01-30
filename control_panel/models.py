from django.contrib.auth.models import User

from django.db import models
from base.models import AbstractBaseAppModel


class AppUser(User, AbstractBaseAppModel):

    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'
        db_table = 't_app_user'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class AppUserSetting(AbstractBaseAppModel):

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    is_email_notification_enabled = models.BooleanField(default=True)
    is_push_notification_enabled = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    font_size = models.PositiveSmallIntegerField(default=14)


    class Meta:
        verbose_name = 'App User Setting'
        verbose_name_plural = 'App User Settings'
        db_table = 't_app_user_setting'

    def __str__(self):
        return f'{self.user.username} - {self.user.email} - user setting'



