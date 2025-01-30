from graphene_django import DjangoObjectType

from talent.models import Talent


class TalentType(DjangoObjectType):
    class Meta:
        model = Talent
