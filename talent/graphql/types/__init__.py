import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from talent.models import Talent


class TalentType(DjangoObjectType):
    class Meta:
        model = Talent


class MatchingResumeType(ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    relevant_skills = graphene.List(graphene.String)
    match_percentage = graphene.String()
    experiences = graphene.List(graphene.String)

    def resolve_first_name(self, info):
        return self.first_name

    def resolve_last_name(self, info):
        return self.last_name

    def resolve_email(self, info):
        return self.email

    def resolve_relevant_skills(self, info):
        return self.relevant_skills

    def resolve_match_percentage(self, info):
        return self.match_percentage

    def resolve_experiences(self, info):
        return self.experiences

