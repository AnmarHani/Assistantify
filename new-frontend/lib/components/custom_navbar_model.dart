import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'custom_navbar_widget.dart' show CustomNavbarWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:just_audio/just_audio.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';

class CustomNavbarModel extends FlutterFlowModel<CustomNavbarWidget> {
  ///  Local state fields for this component.

  bool _isRecording = false;
  set isRecording(bool value) {
    _isRecording = value;
    debugLogWidgetClass(this);
  }

  bool get isRecording => _isRecording;

  ///  State fields for stateful widgets in this component.

  String? recordedAudio;
  FFUploadedFile recordedFileBytes =
      FFUploadedFile(bytes: Uint8List.fromList([]));
  // Stores action output result for [Backend Call - API (Voice )] action in IconButton widget.
  ApiCallResponse? _apiResultyad;
  set apiResultyad(ApiCallResponse? value) {
    _apiResultyad = value;
    debugLogWidgetClass(this);
  }

  ApiCallResponse? get apiResultyad => _apiResultyad;

  AudioPlayer? soundPlayer;
  AudioRecorder? audioRecorder;

  final Map<String, DebugDataField> debugGeneratorVariables = {};
  final Map<String, DebugDataField> debugBackendQueries = {};
  final Map<String, FlutterFlowModel> widgetBuilderComponents = {};
  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {}

  @override
  WidgetClassDebugData toWidgetClassDebugData() => WidgetClassDebugData(
        localStates: {
          'isRecording': debugSerializeParam(
            isRecording,
            ParamType.bool,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=CustomNavbar',
            searchReference:
                'reference=QiUKFAoLaXNSZWNvcmRpbmcSBXdraWxrKgcSBWZhbHNlcgQIBSABUABaC2lzUmVjb3JkaW5nYgxDdXN0b21OYXZiYXI=',
            name: 'bool',
            nullable: false,
          )
        },
        actionOutputs: {
          'recordedAudio': debugSerializeParam(
            recordedAudio,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=CustomNavbar',
            name: 'String',
            nullable: true,
          ),
          'apiResultyad': debugSerializeParam(
            apiResultyad,
            ParamType.ApiResponse,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=CustomNavbar',
            name: 'ApiCallResponse',
            nullable: true,
          )
        },
        generatorVariables: debugGeneratorVariables,
        backendQueries: debugBackendQueries,
        componentStates: {
          ...widgetBuilderComponents.map(
            (key, value) => MapEntry(
              key,
              value.toWidgetClassDebugData(),
            ),
          ),
        }.withoutNulls,
        link:
            'https://app.flutterflow.io/project/assistentify-b1d861/tab=uiBuilder&page=CustomNavbar',
        searchReference: 'reference=OgxDdXN0b21OYXZiYXJQAFoMQ3VzdG9tTmF2YmFy',
        widgetClassName: 'CustomNavbar',
      );
}
