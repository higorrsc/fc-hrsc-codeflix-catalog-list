from typing import List

from src._shared.domain.entity import Entity
from src._shared.domain.repository import Repository
from src._shared.listing import ListInput, ListOutput, ListOutputMeta


class ListEntity[T: Entity]:
    """
    Use case for listing entities.

    Attributes:
        _repository (Repository[T]): The repository for the entities to be listed.
    """

    def __init__(self, repository: Repository[T]) -> None:
        """
        Initializes a new instance of the ListEntity class.

        Args:
            repository (Repository[T]): The repository for the entities to be listed.
        """

        self._repository = repository

    def execute(self, params: ListInput) -> ListOutput[T]:
        """
        Executes the ListEntity use case.

        Args:
            params (ListInput): The input parameters for the use case.

        Returns:
            ListOutput[T]: The output of the use case with the list of entities and the metadata.
        """

        entities: List[T] = self._repository.search(
            page=params.page,
            per_page=params.per_page,
            sort=params.sort.value,  # type: ignore
            direction=params.direction,
            search=params.search,
        )

        meta = ListOutputMeta(
            page=params.page,
            per_page=params.per_page,
            sort=params.sort.value,  # type: ignore
            direction=params.direction,
        )

        return ListOutput(
            data=entities,
            meta=meta,
        )
