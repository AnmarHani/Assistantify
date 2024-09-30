import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:simple_gradient_text/simple_gradient_text.dart';
import 'welcome_page_model.dart';
export 'welcome_page_model.dart';

class WelcomePageWidget extends StatefulWidget {
  const WelcomePageWidget({super.key, this.addModelFn});

  final Function(FlutterFlowModel)? addModelFn;

  @override
  State<WelcomePageWidget> createState() => _WelcomePageWidgetState();
}

class _WelcomePageWidgetState extends State<WelcomePageWidget> with RouteAware {
  late WelcomePageModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => WelcomePageModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    routeObserver.subscribe(this, DebugModalRoute.of(context)!);
    debugLogGlobalProperty(context);
  }

  @override
  void didPopNext() {
    safeSetState(() => _model.isRouteVisible = true);
    debugLogWidgetClass(_model);
  }

  @override
  void didPush() {
    safeSetState(() => _model.isRouteVisible = true);
    debugLogWidgetClass(_model);
  }

  @override
  void didPop() {
    _model.isRouteVisible = false;
  }

  @override
  void didPushNext() {
    _model.isRouteVisible = false;
  }

  @override
  Widget build(BuildContext context) {
    widget.addModelFn?.call(_model);
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primary,
        body: Column(
          mainAxisSize: MainAxisSize.max,
          children: [
            Align(
              alignment: AlignmentDirectional(0.0, 0.0),
              child: Container(
                width: double.infinity,
                height: 460.0,
                decoration: BoxDecoration(),
                alignment: AlignmentDirectional(0.0, 1.0),
                child: Stack(
                  children: [
                    Opacity(
                      opacity: 0.8,
                      child: Align(
                        alignment: AlignmentDirectional(0.0, 0.3),
                        child: Container(
                          width: 272.0,
                          height: 200.0,
                          decoration: BoxDecoration(
                            boxShadow: [
                              BoxShadow(
                                blurRadius: 150.0,
                                color: Color(0xB3CE6AF2),
                                offset: Offset(
                                  0.0,
                                  4.0,
                                ),
                              )
                            ],
                            shape: BoxShape.rectangle,
                          ),
                          alignment: AlignmentDirectional(0.0, 0.0),
                        ),
                      ),
                    ),
                    Align(
                      alignment: AlignmentDirectional(0.0, 0.76),
                      child: Container(
                        width: 404.0,
                        height: 288.54,
                        decoration: BoxDecoration(),
                        child: Column(
                          mainAxisSize: MainAxisSize.max,
                          children: [
                            Align(
                              alignment: AlignmentDirectional(0.0, 0.0),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(8.0),
                                child: Image.asset(
                                  'assets/images/Logo.png',
                                  width: 272.0,
                                  height: 218.54,
                                  fit: BoxFit.fill,
                                ),
                              ),
                            ),
                            Align(
                              alignment: AlignmentDirectional(0.0, 0.0),
                              child: Padding(
                                padding: EdgeInsetsDirectional.fromSTEB(
                                    0.0, 18.0, 0.0, 0.0),
                                child: GradientText(
                                  'Assistantify',
                                  textAlign: TextAlign.justify,
                                  style: FlutterFlowTheme.of(context)
                                      .bodySmall
                                      .override(
                                        fontFamily: 'Telegrafico',
                                        fontSize: 40.0,
                                        letterSpacing: 7.0,
                                        fontWeight: FontWeight.w300,
                                        useGoogleFonts: GoogleFonts.asMap()
                                            .containsKey('Telegrafico'),
                                      ),
                                  colors: [
                                    Color(0xFF2F6FED),
                                    Color(0xFFC54DEF)
                                  ],
                                  gradientDirection: GradientDirection.ttb,
                                  gradientType: GradientType.linear,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Align(
              alignment: AlignmentDirectional(0.0, 0.0),
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0.0, 60.0, 0.0, 0.0),
                child: Container(
                  width: double.infinity,
                  height: 100.0,
                  decoration: BoxDecoration(),
                  child: Align(
                    alignment: AlignmentDirectional(0.0, 0.0),
                    child: GradientText(
                      'Make your life easier with our\n personal assistant product',
                      textAlign: TextAlign.center,
                      style: FlutterFlowTheme.of(context).bodyMedium.override(
                            fontFamily: 'Quantico',
                            color: FlutterFlowTheme.of(context)
                                .secondaryBackground,
                            fontSize: 20.0,
                            letterSpacing: 0.0,
                            useGoogleFonts:
                                GoogleFonts.asMap().containsKey('Quantico'),
                          ),
                      colors: [Color(0xFFB0B0B0), Color(0xFFC6C6C6)],
                      gradientDirection: GradientDirection.ttb,
                      gradientType: GradientType.linear,
                    ),
                  ),
                ),
              ),
            ),
            Container(
              width: 246.0,
              height: 59.0,
              decoration: BoxDecoration(
                boxShadow: [
                  BoxShadow(
                    blurRadius: 6.0,
                    color: Color(0x80000000),
                    offset: Offset(
                      0.0,
                      10.0,
                    ),
                  )
                ],
                gradient: LinearGradient(
                  colors: [
                    Color(0x4C2F6FED),
                    Color(0x4D9963F2),
                    Color(0x4DC54DEF)
                  ],
                  stops: [0.0, 0.65, 1.0],
                  begin: AlignmentDirectional(-1.0, 0.34),
                  end: AlignmentDirectional(1.0, -0.34),
                ),
                borderRadius: BorderRadius.circular(30.0),
              ),
              child: Align(
                alignment: AlignmentDirectional(0.0, 0.0),
                child: FFButtonWidget(
                  onPressed: () async {
                    context.pushNamed('registerPage');
                  },
                  text: 'Create Account',
                  options: FFButtonOptions(
                    width: 246.0,
                    height: 59.0,
                    padding: EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 0.0),
                    iconPadding:
                        EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 0.0),
                    color: Color(0x00FFFFFF),
                    textStyle: FlutterFlowTheme.of(context).titleSmall.override(
                          fontFamily:
                              FlutterFlowTheme.of(context).titleSmallFamily,
                          color: Color(0xFFD6D6D6),
                          fontSize: 24.0,
                          letterSpacing: 0.0,
                          fontWeight: FontWeight.normal,
                          useGoogleFonts: GoogleFonts.asMap().containsKey(
                              FlutterFlowTheme.of(context).titleSmallFamily),
                        ),
                    elevation: 0.0,
                    borderSide: BorderSide(
                      width: 0.0,
                    ),
                    borderRadius: BorderRadius.circular(24.0),
                  ),
                ),
              ),
            ),
            Padding(
              padding: EdgeInsetsDirectional.fromSTEB(0.0, 20.0, 0.0, 0.0),
              child: Container(
                width: 246.0,
                height: 59.0,
                decoration: BoxDecoration(
                  boxShadow: [
                    BoxShadow(
                      blurRadius: 6.0,
                      color: Colors.black,
                      offset: Offset(
                        0.0,
                        4.0,
                      ),
                    )
                  ],
                  gradient: LinearGradient(
                    colors: [
                      Color(0x4C2F6FED),
                      Color(0x4C9963F2),
                      Color(0x4CC54DEF)
                    ],
                    stops: [0.0, 0.65, 1.0],
                    begin: AlignmentDirectional(-1.0, 0.34),
                    end: AlignmentDirectional(1.0, -0.34),
                  ),
                  borderRadius: BorderRadius.circular(30.0),
                ),
                child: Align(
                  alignment: AlignmentDirectional(0.0, 0.0),
                  child: Padding(
                    padding: EdgeInsets.all(2.0),
                    child: FFButtonWidget(
                      onPressed: () async {
                        context.pushNamed('LoginPage');
                      },
                      text: 'LogIn',
                      options: FFButtonOptions(
                        width: 246.0,
                        height: 59.0,
                        padding:
                            EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 0.0),
                        iconPadding:
                            EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 0.0),
                        color: FlutterFlowTheme.of(context).primary,
                        textStyle: FlutterFlowTheme.of(context)
                            .titleSmall
                            .override(
                              fontFamily:
                                  FlutterFlowTheme.of(context).titleSmallFamily,
                              color: Color(0xFFD6D6D6),
                              fontSize: 24.0,
                              letterSpacing: 0.0,
                              fontWeight: FontWeight.normal,
                              useGoogleFonts: GoogleFonts.asMap().containsKey(
                                  FlutterFlowTheme.of(context)
                                      .titleSmallFamily),
                            ),
                        elevation: 0.0,
                        borderSide: BorderSide(
                          width: 0.0,
                        ),
                        borderRadius: BorderRadius.circular(30.0),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
