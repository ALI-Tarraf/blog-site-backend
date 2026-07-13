import graphene
from core.queries import Query
from core.mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)