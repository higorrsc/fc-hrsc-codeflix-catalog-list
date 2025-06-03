import strawberry

from src._shared.listing import ListOutputMeta


@strawberry.experimental.pydantic.type(model=ListOutputMeta, all_fields=True)
class Meta:
    """
    Meta GraphQL type
    """


@strawberry.type
class Result[T]:
    """
    Result GraphQL type
    """

    data: list[T]
    meta: Meta
