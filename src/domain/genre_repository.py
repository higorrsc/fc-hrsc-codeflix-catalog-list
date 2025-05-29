from abc import ABC

from src._shared.domain.repository import Repository
from src.domain.genre import Genre


class GenreRepository(Repository[Genre], ABC):
    """
    GenreRepository interface for interacting with genres in the database.
    """
