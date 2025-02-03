import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from talent.models import Talent


class TalentType(DjangoObjectType):
    class Meta:
        model = Talent


class ResumeType(ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

    def resolve_first_name(self, info):
        return self.first_name

    def resolve_last_name(self, info):
        return self.last_name

    def resolve_email(self, info):
        return self.email

