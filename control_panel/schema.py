import graphene

from control_panel.graphql.mutations import Mutation
from control_panel.graphql.queries import Query


schema = graphene.Schema(query=Query, mutation=Mutation)

