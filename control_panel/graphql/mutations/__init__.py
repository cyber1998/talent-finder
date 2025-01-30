import graphene

from control_panel.graphql.types import AppUserType
from control_panel.models import AppUser


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