import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from src.infra.api._shared.graphql import Result
from src.infra.api.graphql.schema.cast_member import CastMemberGraphQL, get_cast_members
from src.infra.api.graphql.schema.category import CategoryGraphQL, get_categories


@strawberry.type
class Query:
    """
    Query GraphQL type
    """

    categories: Result[CategoryGraphQL] = strawberry.field(resolver=get_categories)
    cast_members: Result[CastMemberGraphQL] = strawberry.field(
        resolver=get_cast_members
    )


schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)
