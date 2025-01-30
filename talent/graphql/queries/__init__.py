import graphene

from talent.graphql.types import TalentType
from talent.models import Talent


class Query(graphene.ObjectType):
    talents = graphene.List(TalentType)
    talent = graphene.Field(TalentType, id=graphene.Int())

    def resolve_talents(self, info, **kwargs):
        return Talent.objects.all()

    def resolve_talent(self, info, id):
        return Talent.objects.get(id=id)