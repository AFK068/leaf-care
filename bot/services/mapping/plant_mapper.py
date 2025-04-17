from typing import ClassVar

from bot.protos.predict import predict_pb2


class ModelMapper:
    """A class to map plant names to their corresponding Plant enum values.

    This class provides a method to get the Plant enum value based on the plant name.
    """

    PLANT_TYPE_MAPPING: ClassVar[dict[str, predict_pb2.Plant]] = {
        "помидор": predict_pb2.PLANT_TOMATO,
        "огурец": predict_pb2.PLANT_CUCUMBER,
        "дыня": predict_pb2.PLANT_MELON,
        "арбуз": predict_pb2.PLANT_WATERMELON,
        "клубника": predict_pb2.PLANT_STRAWBERRY,
        "перец": predict_pb2.PLANT_PEPPER,
    }

    @classmethod
    def get_plant_type(cls, plant_name: str) -> predict_pb2.Plant:
        plant_name = plant_name.strip()
        plant_name = plant_name.lower()

        plant_type = cls.PLANT_TYPE_MAPPING.get(plant_name)
        if plant_type is None:
            error_msg = f"Unknown plant name: {plant_name}"
            raise ValueError(error_msg)
        return plant_type
