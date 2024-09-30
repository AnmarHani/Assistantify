import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'register_page_widget.dart' show RegisterPageWidget;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:simple_gradient_text/simple_gradient_text.dart';

class RegisterPageModel extends FlutterFlowModel<RegisterPageWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for email widget.
  FocusNode? emailFocusNode;
  TextEditingController? emailTextController;
  String? Function(BuildContext, String?)? emailTextControllerValidator;
  // State field(s) for username widget.
  FocusNode? usernameFocusNode;
  TextEditingController? usernameTextController;
  String? Function(BuildContext, String?)? usernameTextControllerValidator;
  // State field(s) for password widget.
  FocusNode? passwordFocusNode;
  TextEditingController? passwordTextController;
  late bool passwordVisibility;
  String? Function(BuildContext, String?)? passwordTextControllerValidator;
  // Stores action output result for [Backend Call - API (Register)] action in registerBtn widget.
  ApiCallResponse? _apiResultlld;
  set apiResultlld(ApiCallResponse? value) {
    _apiResultlld = value;
    debugLogWidgetClass(this);
  }

  ApiCallResponse? get apiResultlld => _apiResultlld;

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
    emailFocusNode?.dispose();
    emailTextController?.dispose();

    usernameFocusNode?.dispose();
    usernameTextController?.dispose();

    passwordFocusNode?.dispose();
    passwordTextController?.dispose();
  }

  @override
  WidgetClassDebugData toWidgetClassDebugData() => WidgetClassDebugData(
        widgetParameters: {
          'username': debugSerializeParam(
            widget?.username,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=registerPage',
            searchReference:
                'reference=ShgKEgoIdXNlcm5hbWUSBm0xcmw1cnICCANQAVoIdXNlcm5hbWU=',
            name: 'String',
            nullable: true,
          )
        }.withoutNulls,
        widgetStates: {
          'emailText': debugSerializeParam(
            emailTextController?.text,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=registerPage',
            name: 'String',
            nullable: true,
          ),
          'usernameText': debugSerializeParam(
            usernameTextController?.text,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=registerPage',
            name: 'String',
            nullable: true,
          ),
          'passwordText': debugSerializeParam(
            passwordTextController?.text,
            ParamType.String,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=registerPage',
            name: 'String',
            nullable: true,
          )
        },
        actionOutputs: {
          'apiResultlld': debugSerializeParam(
            apiResultlld,
            ParamType.ApiResponse,
            link:
                'https://app.flutterflow.io/project/assistentify-b1d861?tab=uiBuilder&page=registerPage',
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
            'https://app.flutterflow.io/project/assistentify-b1d861/tab=uiBuilder&page=registerPage',
        searchReference: 'reference=OgxyZWdpc3RlclBhZ2VQAVoMcmVnaXN0ZXJQYWdl',
        widgetClassName: 'registerPage',
      );
}
