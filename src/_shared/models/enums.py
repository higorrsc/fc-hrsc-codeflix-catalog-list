from enum import StrEnum


class Rating(StrEnum):
    """
    A enum representing a rating.
    """

    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"


class Operation(StrEnum):
    """
    A enum representing an kafka operation.
    """

    CREATE = "c"
    UPDATE = "u"
    DELETE = "d"
    READ = "r"
