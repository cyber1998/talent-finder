import graphene
from talent.schema import Query as TalentQuery
from control_panel.schema import (
    Query as ControlPanelQuery,
    Mutation as TalentMutation
)

class Query(
    TalentQuery,
    ControlPanelQuery,
    graphene.ObjectType):
    pass

class Mutation(TalentMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
