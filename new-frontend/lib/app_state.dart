import 'package:flutter/material.dart';
import '/backend/schema/structs/index.dart';
import 'backend/api_requests/api_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'flutter_flow/flutter_flow_util.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {}

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  String _UserToken = '';
  String get UserToken => _UserToken;
  set UserToken(String value) {
    _UserToken = value;

    debugLogAppState(this);
  }

  String _username = '';
  String get username => _username;
  set username(String value) {
    _username = value;

    debugLogAppState(this);
  }

  String _coins = '';
  String get coins => _coins;
  set coins(String value) {
    _coins = value;

    debugLogAppState(this);
  }

  late LoggableList<ChatHistoryTypeStruct> _chatHistory = LoggableList([
    ChatHistoryTypeStruct.fromSerializableMap(jsonDecode(
        '{\"userMessageType\":\"Hello World\",\"botMessageType\":\"Hi!\"}'))
  ]);
  List<ChatHistoryTypeStruct> get chatHistory =>
      _chatHistory?..logger = () => debugLogAppState(this);
  set chatHistory(List<ChatHistoryTypeStruct> value) {
    if (value != null) {
      _chatHistory = LoggableList(value);
    }

    debugLogAppState(this);
  }

  void addToChatHistory(ChatHistoryTypeStruct value) {
    chatHistory.add(value);
  }

  void removeFromChatHistory(ChatHistoryTypeStruct value) {
    chatHistory.remove(value);
  }

  void removeAtIndexFromChatHistory(int index) {
    chatHistory.removeAt(index);
  }

  void updateChatHistoryAtIndex(
    int index,
    ChatHistoryTypeStruct Function(ChatHistoryTypeStruct) updateFn,
  ) {
    chatHistory[index] = updateFn(_chatHistory[index]);
  }

  void insertAtIndexInChatHistory(int index, ChatHistoryTypeStruct value) {
    chatHistory.insert(index, value);
  }

  Map<String, DebugDataField> toDebugSerializableMap() => {
        'UserToken': debugSerializeParam(
          UserToken,
          ParamType.String,
          link:
              'https://app.flutterflow.io/project/assistentify-b1d861?tab=appValues&appValuesTab=state',
          searchReference:
              'reference=ChsKFQoJVXNlclRva2VuEghnZzhqNWRxbnICCANaCVVzZXJUb2tlbg==',
          name: 'String',
          nullable: false,
        ),
        'username': debugSerializeParam(
          username,
          ParamType.String,
          link:
              'https://app.flutterflow.io/project/assistentify-b1d861?tab=appValues&appValuesTab=state',
          searchReference:
              'reference=ChoKFAoIdXNlcm5hbWUSCDZnb2w1aXlscgIIA1oIdXNlcm5hbWU=',
          name: 'String',
          nullable: false,
        ),
        'coins': debugSerializeParam(
          coins,
          ParamType.String,
          link:
              'https://app.flutterflow.io/project/assistentify-b1d861?tab=appValues&appValuesTab=state',
          searchReference:
              'reference=ChcKEQoFY29pbnMSCHl6aDlmZ3JxcgIIA1oFY29pbnM=',
          name: 'String',
          nullable: false,
        ),
        'chatHistory': debugSerializeParam(
          chatHistory,
          ParamType.DataStruct,
          isList: true,
          link:
              'https://app.flutterflow.io/project/assistentify-b1d861?tab=appValues&appValuesTab=state',
          searchReference:
              'reference=CjsKFwoLY2hhdEhpc3RvcnkSCGY4MzJjZmt2ciASAggUKhoSGAoPY2hhdEhpc3RvcnlUeXBlEgVobjFra1oLY2hhdEhpc3Rvcnk=',
          name: 'chatHistoryType',
          nullable: false,
        )
      };
}
