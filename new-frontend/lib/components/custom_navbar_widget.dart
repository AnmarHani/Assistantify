import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:just_audio/just_audio.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';
import 'custom_navbar_model.dart';
export 'custom_navbar_model.dart';

class CustomNavbarWidget extends StatefulWidget {
  const CustomNavbarWidget({super.key, this.addModelFn});

  final Function(FlutterFlowModel)? addModelFn;

  @override
  State<CustomNavbarWidget> createState() => _CustomNavbarWidgetState();
}

class _CustomNavbarWidgetState extends State<CustomNavbarWidget>
    with RouteAware {
  late CustomNavbarModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => CustomNavbarModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    widget.addModelFn?.call(_model);
    return Container(
      width: double.infinity,
      height: 127.0,
      decoration: BoxDecoration(),
      child: Stack(
        alignment: AlignmentDirectional(0.0, 1.0),
        children: [
          Align(
            alignment: AlignmentDirectional(0.0, 1.0),
            child: Container(
              width: double.infinity,
              height: 80.0,
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).primary,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(0.0),
                  bottomRight: Radius.circular(0.0),
                  topLeft: Radius.circular(0.0),
                  topRight: Radius.circular(0.0),
                ),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Align(
                    alignment: AlignmentDirectional(0.0, -1.0),
                    child: Container(
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: Color(0xFF23272F),
                      ),
                    ),
                  ),
                  Expanded(
                    child: Align(
                      alignment: AlignmentDirectional(0.0, 0.0),
                      child: Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(
                            10.0, 0.0, 10.0, 0.0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            FlutterFlowIconButton(
                              borderColor: Colors.transparent,
                              borderRadius: 8.0,
                              fillColor: FlutterFlowTheme.of(context).primary,
                              icon: Icon(
                                Icons.home,
                                color: FlutterFlowTheme.of(context).info,
                                size: 34.0,
                              ),
                              onPressed: () async {
                                context.pushNamed('HomePage');
                              },
                            ),
                            FlutterFlowIconButton(
                              borderColor: Colors.transparent,
                              borderRadius: 8.0,
                              icon: Icon(
                                Icons.analytics_outlined,
                                color: FlutterFlowTheme.of(context).info,
                                size: 34.0,
                              ),
                              onPressed: () async {
                                context.pushNamed('HomePage');
                              },
                            ),
                            FlutterFlowIconButton(
                              borderColor: Colors.transparent,
                              borderRadius: 8.0,
                              fillColor: FlutterFlowTheme.of(context).primary,
                              icon: Icon(
                                Icons.card_giftcard,
                                color: FlutterFlowTheme.of(context).info,
                                size: 34.0,
                              ),
                              onPressed: () async {
                                context.pushNamed('HomePage');
                              },
                            ),
                            FlutterFlowIconButton(
                              borderColor: Colors.transparent,
                              borderRadius: 8.0,
                              fillColor: FlutterFlowTheme.of(context).primary,
                              icon: Icon(
                                Icons.person_2,
                                color: FlutterFlowTheme.of(context).info,
                                size: 34.0,
                              ),
                              onPressed: () async {
                                context.pushNamed('profilePage');
                              },
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Align(
            alignment: AlignmentDirectional(0.0, -0.7),
            child: Container(
              width: 85.0,
              height: 85.0,
              decoration: BoxDecoration(
                color: Color(0xFF342647),
                boxShadow: [
                  BoxShadow(
                    blurRadius: 10.0,
                    color: Colors.black,
                    offset: Offset(
                      0.0,
                      2.0,
                    ),
                  )
                ],
                shape: BoxShape.circle,
              ),
              child: Builder(
                builder: (context) {
                  if (_model.isRecording) {
                    return FlutterFlowIconButton(
                      borderRadius: 100.0,
                      fillColor: FlutterFlowTheme.of(context).accent1,
                      icon: Icon(
                        Icons.stop_circle_sharp,
                        color: FlutterFlowTheme.of(context).info,
                        size: 50.0,
                      ),
                      onPressed: () async {
                        await stopAudioRecording(
                          audioRecorder: _model.audioRecorder,
                          audioName: 'recordedFileBytes.mp3',
                          onRecordingComplete: (audioFilePath, audioBytes) {
                            _model.recordedAudio = audioFilePath;
                            _model.recordedFileBytes = audioBytes;
                          },
                        );

                        _model.isRecording = false;
                        safeSetState(() {});
                        _model.apiResultyad = await VoiceCall.call(
                          audioFile: _model.recordedAudio,
                        );

                        if ((_model.apiResultyad?.succeeded ?? true)) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                'Success',
                                style: TextStyle(
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                ),
                              ),
                              duration: Duration(milliseconds: 4000),
                              backgroundColor:
                                  FlutterFlowTheme.of(context).secondary,
                            ),
                          );
                          _model.soundPlayer ??= AudioPlayer();
                          if (_model.soundPlayer!.playing) {
                            await _model.soundPlayer!.stop();
                          }
                          _model.soundPlayer!.setVolume(1.0);
                          _model.soundPlayer!
                              .setUrl(getJsonField(
                                (_model.apiResultyad?.jsonBody ?? ''),
                                r'''$.file_path''',
                              ).toString())
                              .then((_) => _model.soundPlayer!.play());
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                'Failed',
                                style: TextStyle(
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                ),
                              ),
                              duration: Duration(milliseconds: 4000),
                              backgroundColor:
                                  FlutterFlowTheme.of(context).error,
                            ),
                          );
                        }

                        safeSetState(() {});
                      },
                    );
                  } else {
                    return Align(
                      alignment: AlignmentDirectional(0.0, 0.0),
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: InkWell(
                          splashColor: Colors.transparent,
                          focusColor: Colors.transparent,
                          hoverColor: Colors.transparent,
                          highlightColor: Colors.transparent,
                          onTap: () async {
                            _model.isRecording = true;
                            safeSetState(() {});
                            await startAudioRecording(
                              context,
                              audioRecorder: _model.audioRecorder ??=
                                  AudioRecorder(),
                            );
                          },
                          child: Container(
                            width: double.infinity,
                            height: double.infinity,
                            clipBehavior: Clip.antiAlias,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                            ),
                            child: Image.asset(
                              'assets/images/Logo.png',
                              fit: BoxFit.contain,
                            ),
                          ),
                        ),
                      ),
                    );
                  }
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
