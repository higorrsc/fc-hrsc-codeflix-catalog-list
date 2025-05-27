from abc import ABC

from src._shared.domain.repository import Repository
from src.domain.category import Category


class CategoryRepository(Repository[Category], ABC):
    """
    CategoryRepository interface for interacting with categories in the database.
    """
