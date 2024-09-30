// ignore_for_file: unnecessary_getters_setters

import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class ChatHistoryTypeStruct extends BaseStruct {
  ChatHistoryTypeStruct({
    String? userMessageType,
    String? botMessageType,
  })  : _userMessageType = userMessageType,
        _botMessageType = botMessageType;

  // "userMessageType" field.
  String? _userMessageType;
  String get userMessageType => _userMessageType ?? '';
  set userMessageType(String? val) {
    _userMessageType = val;
    debugLog();
  }

  bool hasUserMessageType() => _userMessageType != null;

  // "botMessageType" field.
  String? _botMessageType;
  String get botMessageType => _botMessageType ?? '';
  set botMessageType(String? val) {
    _botMessageType = val;
    debugLog();
  }

  bool hasBotMessageType() => _botMessageType != null;

  static ChatHistoryTypeStruct fromMap(Map<String, dynamic> data) =>
      ChatHistoryTypeStruct(
        userMessageType: data['userMessageType'] as String?,
        botMessageType: data['botMessageType'] as String?,
      );

  static ChatHistoryTypeStruct? maybeFromMap(dynamic data) => data is Map
      ? ChatHistoryTypeStruct.fromMap(data.cast<String, dynamic>())
      : null;

  Map<String, dynamic> toMap() => {
        'userMessageType': _userMessageType,
        'botMessageType': _botMessageType,
      }.withoutNulls;

  @override
  Map<String, dynamic> toSerializableMap() => {
        'userMessageType': serializeParam(
          _userMessageType,
          ParamType.String,
        ),
        'botMessageType': serializeParam(
          _botMessageType,
          ParamType.String,
        ),
      }.withoutNulls;

  static ChatHistoryTypeStruct fromSerializableMap(Map<String, dynamic> data) =>
      ChatHistoryTypeStruct(
        userMessageType: deserializeParam(
          data['userMessageType'],
          ParamType.String,
          false,
        ),
        botMessageType: deserializeParam(
          data['botMessageType'],
          ParamType.String,
          false,
        ),
      );
  @override
  Map<String, DebugDataField> toDebugSerializableMap() => {
        'userMessageType': debugSerializeParam(
          userMessageType,
          ParamType.String,
          name: 'String',
          nullable: false,
        ),
        'botMessageType': debugSerializeParam(
          botMessageType,
          ParamType.String,
          name: 'String',
          nullable: false,
        ),
      };

  @override
  String toString() => 'ChatHistoryTypeStruct(${toMap()})';

  @override
  bool operator ==(Object other) {
    return other is ChatHistoryTypeStruct &&
        userMessageType == other.userMessageType &&
        botMessageType == other.botMessageType;
  }

  @override
  int get hashCode =>
      const ListEquality().hash([userMessageType, botMessageType]);
}

ChatHistoryTypeStruct createChatHistoryTypeStruct({
  String? userMessageType,
  String? botMessageType,
}) =>
    ChatHistoryTypeStruct(
      userMessageType: userMessageType,
      botMessageType: botMessageType,
    );
