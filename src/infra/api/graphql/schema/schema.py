from uuid import UUID

import strawberry
from strawberry.fastapi import GraphQLRouter

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import SortDirection
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.infra.api._shared.dependencies import get_category_repository


@strawberry.type
class CategoryGraphQL:
    id: UUID
    name: str
    description: str = ""


@strawberry.type
class Meta:
    page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    sort: str | None
    direction: SortDirection = SortDirection.ASC


@strawberry.type
class Result[T]:
    data: list[T]
    meta: Meta


def get_categories(
    sort: CategorySortableFields = CategorySortableFields.NAME,
    search: str | None = None,
    page: int = 1,
    per_page: int = DEFAULT_PAGINATION_SIZE,
    direction: SortDirection = SortDirection.ASC,
) -> Result[CategoryGraphQL]:
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
        data=[
            CategoryGraphQL(
                id=category.id,
                name=category.name,
                description=category.description,
            )
            for category in output.data
        ],
        meta=Meta(
            page=output.meta.page,
            per_page=output.meta.per_page,
            sort=output.meta.sort,
            direction=output.meta.direction,
        ),
    )


@strawberry.type
class Query:
    categories: Result[CategoryGraphQL] = strawberry.field(resolver=get_categories)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
