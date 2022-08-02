from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def enum_to_list(cls):
        return list(map(lambda c: c.value, cls))


class InputEnums(BaseEnum):
    ID = "ID"
    REALEASE_DATE = "release date"
    GAME_NAME = "game name"
    COUNTRY_CODE = "couontry code"
    NBR_COPY = "number of copy"
    PRICE = "price"

class OutputEnum(Enum):
    ID = "ID"
    REALEASE_DATE = "release date"
    GAME_NAME = "Name"
    COUNTRY = "country"
    NBR_COPY = "copies sold"
    PRICE = "price"
    REVENUE = "Total Revenue"