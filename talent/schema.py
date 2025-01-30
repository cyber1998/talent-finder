import graphene
from talent.graphql.queries import Query

schema = graphene.Schema(query=Query, mutation=None)