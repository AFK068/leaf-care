from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Plant(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLANT_TOMATO: _ClassVar[Plant]
    PLANT_CUCUMBER: _ClassVar[Plant]
    PLANT_SALAD: _ClassVar[Plant]
    PLANT_MELON: _ClassVar[Plant]
    PLANT_WATERMELON: _ClassVar[Plant]
    PLANT_STRAWBERRY: _ClassVar[Plant]
    PLANT_PEPPER: _ClassVar[Plant]
PLANT_TOMATO: Plant
PLANT_CUCUMBER: Plant
PLANT_SALAD: Plant
PLANT_MELON: Plant
PLANT_WATERMELON: Plant
PLANT_STRAWBERRY: Plant
PLANT_PEPPER: Plant

class ClassProbability(_message.Message):
    __slots__ = ("class_name", "probability")
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    probability: float
    def __init__(self, class_name: _Optional[str] = ..., probability: _Optional[float] = ...) -> None: ...

class ImageResults(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[ClassProbability]
    def __init__(self, results: _Optional[_Iterable[_Union[ClassProbability, _Mapping]]] = ...) -> None: ...

class PredictorRequest(_message.Message):
    __slots__ = ("image_data", "plant")
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    PLANT_FIELD_NUMBER: _ClassVar[int]
    image_data: _containers.RepeatedScalarFieldContainer[bytes]
    plant: Plant
    def __init__(self, image_data: _Optional[_Iterable[bytes]] = ..., plant: _Optional[_Union[Plant, str]] = ...) -> None: ...

class PredictorReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[ImageResults]
    def __init__(self, result: _Optional[_Iterable[_Union[ImageResults, _Mapping]]] = ...) -> None: ...
