import graphene
from graphene_django.types import DjangoObjectType

from control_panel.models import AppUser, AppUserSetting


class AppUserSettingType(DjangoObjectType):
    class Meta:
        model = AppUserSetting

class AppUserType(DjangoObjectType):

    setting = graphene.Field(AppUserSettingType)

    class Meta:
        model = AppUser

    def resolve_setting(self, info):
        return AppUserSetting.objects.get(user=self.id)


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

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        is_superuser = graphene.String(required=False)

    user = graphene.Field(AppUserType)

    def mutate(self, info, username, password, email, first_name, last_name, is_superuser):

        user = AppUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser
        )
        return CreateUserMutation(user=user)

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(AppUserType)

    def mutate(self, info, **kwargs):
        user = AppUser.objects.get(id=kwargs['id'])
        for key, value in kwargs.items():
            if value:
                setattr(user, key, value)
        user.save()
        return UpdateUserMutation(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()


schema = graphene.Schema(query=Query)

