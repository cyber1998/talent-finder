import graphene
from talent import schema as TalentSchema
from control_panel import schema as ControlPanelSchema
class Query(
    ControlPanelSchema.Query,
    TalentSchema.Query,
    graphene.ObjectType):
    pass

class Mutation(
    ControlPanelSchema.Mutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
