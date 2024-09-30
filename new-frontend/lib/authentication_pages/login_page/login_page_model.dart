import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'login_page_widget.dart' show LoginPageWidget;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:simple_gradient_text/simple_gradient_text.dart';

class LoginPageModel extends FlutterFlowModel<LoginPageWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for userName widget.
  FocusNode? userNameFocusNode;
  TextEditingController? userNameTextController;
  String? Function(BuildContext, String?)? userNameTextControllerValidator;
  // State field(s) for password widget.
  FocusNode? passwordFocusNode;
  TextEditingController? passwordTextController;
  late bool passwordVisibility;
  String? Function(BuildContext, String?)? passwordTextControllerValidator;
  // Stores action output result for [Backend Call - API (Login)] action in Button widget.
  ApiCallResponse? _apiResultqsi;
  set apiResultqsi(ApiCallResponse? value) {
    _apiResultqsi = value;
    debugLogWidgetClass(this);
  }

  ApiCallResponse? get apiResultqsi => _apiResultqsi;

  final Map<String, DebugDataField> debugGeneratorVariables = {};
  final Map<String, DebugDataField> debugBackendQueries = {};
  final Map<String, FlutterFlowModel> widgetBuilderComponents = {};
  @override
  void initState(BuildContext context) {
    passwordVisibility = false;

    debugLogWidgetClass(this);
  }

  @override
  void dispose() {
    userNameFocusNode?.dispose();
    userNameTextController?.dispose();

    passwordFocusNode?.dispose();
    passwordTextController?.dispose();
  }

  @override
  WidgetClassDebugData toWidgetClassDebugData() => WidgetClassDebugData(
        widgetStates: {
          'userNameText': debugSerializeParam(
            userNameTextController?.text,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=LoginPage',
            name: 'String',
            nullable: true,
          ),
          'passwordText': debugSerializeParam(
            passwordTextController?.text,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=LoginPage',
            name: 'String',
            nullable: true,
          )
        },
        actionOutputs: {
          'apiResultqsi': debugSerializeParam(
            apiResultqsi,
            ParamType.ApiResponse,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=LoginPage',
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
            'https://app.flutterflow.io/project/assistentify-b1d861/tab=uiBuilder&page=LoginPage',
        searchReference: 'reference=OglMb2dpblBhZ2VQAVoJTG9naW5QYWdl',
        widgetClassName: 'LoginPage',
      );
}
