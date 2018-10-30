# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service_specs/moses_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service_specs/moses_service.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n!service_specs/moses_service.proto\"F\n\x0f\x43rossValOptions\x12\r\n\x05\x66olds\x18\x01 \x01(\x05\x12\x10\n\x08testSize\x18\x02 \x01(\x02\x12\x12\n\nrandomSeed\x18\x03 \x01(\x05\"\x8f\x01\n\x12\x41nalysisParameters\x12\x13\n\tmosesOpts\x18\x01 \x01(\tH\x00\x12(\n\x0c\x63rossValOpts\x18\x02 \x01(\x0b\x32\x10.CrossValOptionsH\x00\x12\x12\n\x08\x63\x61tegory\x18\x03 \x01(\tH\x00\x12\x11\n\x07\x64\x61taset\x18\x04 \x01(\x0cH\x00\x42\x13\n\x11one_of_parameters\"0\n\x06Result\x12\x11\n\tresultUrl\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t2A\n\x0cMosesService\x12\x31\n\rStartAnalysis\x12\x13.AnalysisParameters\x1a\x07.Result\"\x00(\x01\x62\x06proto3')
)




_CROSSVALOPTIONS = _descriptor.Descriptor(
  name='CrossValOptions',
  full_name='CrossValOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='folds', full_name='CrossValOptions.folds', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='testSize', full_name='CrossValOptions.testSize', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='randomSeed', full_name='CrossValOptions.randomSeed', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=107,
)


_ANALYSISPARAMETERS = _descriptor.Descriptor(
  name='AnalysisParameters',
  full_name='AnalysisParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mosesOpts', full_name='AnalysisParameters.mosesOpts', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crossValOpts', full_name='AnalysisParameters.crossValOpts', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='category', full_name='AnalysisParameters.category', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataset', full_name='AnalysisParameters.dataset', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='one_of_parameters', full_name='AnalysisParameters.one_of_parameters',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=110,
  serialized_end=253,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultUrl', full_name='Result.resultUrl', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='Result.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=255,
  serialized_end=303,
)

_ANALYSISPARAMETERS.fields_by_name['crossValOpts'].message_type = _CROSSVALOPTIONS
_ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters'].fields.append(
  _ANALYSISPARAMETERS.fields_by_name['mosesOpts'])
_ANALYSISPARAMETERS.fields_by_name['mosesOpts'].containing_oneof = _ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters']
_ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters'].fields.append(
  _ANALYSISPARAMETERS.fields_by_name['crossValOpts'])
_ANALYSISPARAMETERS.fields_by_name['crossValOpts'].containing_oneof = _ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters']
_ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters'].fields.append(
  _ANALYSISPARAMETERS.fields_by_name['category'])
_ANALYSISPARAMETERS.fields_by_name['category'].containing_oneof = _ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters']
_ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters'].fields.append(
  _ANALYSISPARAMETERS.fields_by_name['dataset'])
_ANALYSISPARAMETERS.fields_by_name['dataset'].containing_oneof = _ANALYSISPARAMETERS.oneofs_by_name['one_of_parameters']
DESCRIPTOR.message_types_by_name['CrossValOptions'] = _CROSSVALOPTIONS
DESCRIPTOR.message_types_by_name['AnalysisParameters'] = _ANALYSISPARAMETERS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CrossValOptions = _reflection.GeneratedProtocolMessageType('CrossValOptions', (_message.Message,), dict(
  DESCRIPTOR = _CROSSVALOPTIONS,
  __module__ = 'service_specs.moses_service_pb2'
  # @@protoc_insertion_point(class_scope:CrossValOptions)
  ))
_sym_db.RegisterMessage(CrossValOptions)

AnalysisParameters = _reflection.GeneratedProtocolMessageType('AnalysisParameters', (_message.Message,), dict(
  DESCRIPTOR = _ANALYSISPARAMETERS,
  __module__ = 'service_specs.moses_service_pb2'
  # @@protoc_insertion_point(class_scope:AnalysisParameters)
  ))
_sym_db.RegisterMessage(AnalysisParameters)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'service_specs.moses_service_pb2'
  # @@protoc_insertion_point(class_scope:Result)
  ))
_sym_db.RegisterMessage(Result)



_MOSESSERVICE = _descriptor.ServiceDescriptor(
  name='MosesService',
  full_name='MosesService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=305,
  serialized_end=370,
  methods=[
  _descriptor.MethodDescriptor(
    name='StartAnalysis',
    full_name='MosesService.StartAnalysis',
    index=0,
    containing_service=None,
    input_type=_ANALYSISPARAMETERS,
    output_type=_RESULT,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MOSESSERVICE)

DESCRIPTOR.services_by_name['MosesService'] = _MOSESSERVICE

# @@protoc_insertion_point(module_scope)
