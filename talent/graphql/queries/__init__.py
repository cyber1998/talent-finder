import graphene

from talent.graphql.types import TalentType, MatchingResumeType
from talent.helpers import get_resumes
from talent.models import Talent


class Query(graphene.ObjectType):
    talents = graphene.List(TalentType)
    talent = graphene.Field(TalentType, id=graphene.Int())
    matching_resumes = graphene.List(MatchingResumeType, query=graphene.String(), top_k=graphene.Int())

    def resolve_talents(self, info, **kwargs):
        return Talent.objects.all()

    def resolve_talent(self, info, id):
        return Talent.objects.get(id=id)

    def resolve_matching_resumes(self, info, query, top_k):
        resumes = get_resumes(query, top_k)
        # Convert the results to a list of ResumeType objects
        return [MatchingResumeType(**resume) for resume in resumes]
