import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutputMeta, SortDirection
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.domain.category import Category
from src.infra.api._shared.dependencies import get_category_repository


@strawberry.experimental.pydantic.type(model=Category)
class CategoryGraphQL:
    """
    Category GraphQL type
    """

    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto


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


def get_categories(
    sort: CategorySortableFields = CategorySortableFields.NAME,
    search: str | None = None,
    page: int = 1,
    per_page: int = DEFAULT_PAGINATION_SIZE,
    direction: SortDirection = SortDirection.ASC,
) -> Result[CategoryGraphQL]:
    """
    Retrieves a list of categories

    This resolver uses the ListCategory use case to retrieve and return
    categories. The categories are fetched from an Elasticsearch repository
    and returned in a structured format defined by Result.

    Returns:
        Result[CategoryGraphQL]: A structured list of categories.
    """

    repository = get_category_repository()
    use_case = ListCategory(repository=repository)
    output = use_case.execute(
        ListCategoryInput(
            search=search,
            page=page,
            per_page=per_page,
            sort=sort,
            direction=direction,
        )
    )

    return Result(
        data=[CategoryGraphQL.from_pydantic(category) for category in output.data],
        meta=Meta.from_pydantic(output.meta),  # type: ignore
    )


@strawberry.type
class Query:
    """
    Query GraphQL type
    """

    categories: Result[CategoryGraphQL] = strawberry.field(resolver=get_categories)


schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)
