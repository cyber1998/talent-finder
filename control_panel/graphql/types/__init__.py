import graphene
from graphene_django import DjangoObjectType

from control_panel.models import AppUserSetting, AppUser


class AppUserSettingType(DjangoObjectType):
    class Meta:
        model = AppUserSetting

class AppUserType(DjangoObjectType):

    setting = graphene.Field(AppUserSettingType)

    class Meta:
        model = AppUser

    def resolve_setting(self, info):
        return AppUserSetting.objects.get(user=self.id)