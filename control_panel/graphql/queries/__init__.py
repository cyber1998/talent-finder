import graphene

from control_panel.graphql.types import AppUserType, AppUserSettingType
from control_panel.models import AppUser, AppUserSetting


class Query(graphene.ObjectType):
    users = graphene.List(AppUserType)
    user = graphene.Field(AppUserType, id=graphene.Int())
    settings = graphene.List(AppUserSettingType)
    setting = graphene.Field(AppUserSettingType, id=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return AppUser.objects.all()

    def resolve_user(self, info, id):
        return AppUser.objects.get(id=id)

    def resolve_settings(self, info, **kwargs):
        return AppUserSetting.objects.all()

    def resolve_setting(self, info, id):
        return AppUserSetting.objects.get(id=id)
