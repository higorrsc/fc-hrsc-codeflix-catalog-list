from src._shared.domain.entity import Entity


class Category(Entity):
    """
    Represents a category in the system.
    This class inherits from Entity and includes additional fields
    specific to a category.
    Attributes:
        name (str): The name of the category.
        description (str): A brief description of the category.
    Example:
    category = Category(
        id=UUID("12345678-1234-1234-1234-123456789012"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        name="Electronics",
        description="Devices and gadgets related to electronics."
    )
    """

    name: str
    description: str = ""
