# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: predict.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'predict.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpredict.proto\x12\x07predict\"E\n\x10PredictorRequest\x12\x12\n\nimage_data\x18\x01 \x03(\x0c\x12\x1d\n\x05plant\x18\x02 \x01(\x0e\x32\x0e.predict.Plant\" \n\x0ePredictorReply\x12\x0e\n\x06result\x18\x01 \x03(\t*\x8d\x01\n\x05Plant\x12\x10\n\x0cPLANT_TOMATO\x10\x00\x12\x12\n\x0ePLANT_CUCUMBER\x10\x01\x12\x0f\n\x0bPLANT_SALAD\x10\x02\x12\x0f\n\x0bPLANT_MELON\x10\x03\x12\x14\n\x10PLANT_WATERMELON\x10\x04\x12\x14\n\x10PLANT_STRAWBERRY\x10\x05\x12\x10\n\x0cPLANT_PEPPER\x10\x06\x32L\n\tPredictor\x12?\n\x07Predict\x12\x19.predict.PredictorRequest\x1a\x17.predict.PredictorReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'predict_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PLANT']._serialized_start=132
  _globals['_PLANT']._serialized_end=273
  _globals['_PREDICTORREQUEST']._serialized_start=26
  _globals['_PREDICTORREQUEST']._serialized_end=95
  _globals['_PREDICTORREPLY']._serialized_start=97
  _globals['_PREDICTORREPLY']._serialized_end=129
  _globals['_PREDICTOR']._serialized_start=275
  _globals['_PREDICTOR']._serialized_end=351
# @@protoc_insertion_point(module_scope)
