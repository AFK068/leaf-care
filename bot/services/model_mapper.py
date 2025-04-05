from typing import ClassVar

from bot.protos.predict import predict_pb2


class ModelMapper:
    """A class to map plant names to their corresponding Plant enum values.

    This class provides a method to get the Plant enum value based on the plant name.
    """

    PLANT_TYPE_MAPPING: ClassVar[dict[str, predict_pb2.Plant]] = {
        "Помидор": predict_pb2.PLANT_TOMATO,
        "Огурец": predict_pb2.PLANT_CUCUMBER,
        "Дыня": predict_pb2.PLANT_MELON,
        "Арбуз": predict_pb2.PLANT_WATERMELON,
        "Клубника": predict_pb2.PLANT_STRAWBERRY,
        "Перец": predict_pb2.PLANT_PEPPER,
    }

    @classmethod
    def get_plant_type(cls, plant_name: str) -> predict_pb2.Plant:
        """Map a plant name to its corresponding Plant enum value.

        :param plant_name: The name of the plant.
        :return: The corresponding Plant enum value.
        """
        plant_type = cls.PLANT_TYPE_MAPPING.get(plant_name)
        if not plant_type:
            error_msg = f"Unknown plant name: {plant_name}"
            raise ValueError(error_msg)
        return plant_type
