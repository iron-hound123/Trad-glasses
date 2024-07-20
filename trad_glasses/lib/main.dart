import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:trad_glasses/Screen/camera_app.dart';

late List<CameraDescription> _cameras;
void main() async{
  WidgetsFlutterBinding.ensureInitialized();

  _cameras = await availableCameras();
  runApp(CameraApp(cameras: _cameras));
}
