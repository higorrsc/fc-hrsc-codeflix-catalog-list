from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Category(BaseModel):
    """
    Category model representing a category in the system.
    It includes an ID, name, description, and creation timestamp.

    Attributes:
        - id (UUID): Unique identifier for the category.
        - name (str): Name of the category.
        - description (str): Description of the category.
        - created_at (datetime): Timestamp when the category was created.
        - updated_at (datetime): Timestamp when the category was last updated.
        - is_active (bool): Indicates if the category is active.
    """

    id: UUID
    name: str
    description: str = ""
    created_at: datetime
    updated_at: datetime
    is_active: bool
