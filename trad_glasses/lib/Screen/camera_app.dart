import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:tflite/tflite.dart';

typedef void Callback(List<dynamic> list, int h, int w);

class CameraApp extends StatefulWidget {
  const CameraApp({super.key, required this.cameras, required this.model});
  final List<CameraDescription> cameras;
  final String model;
  @override
  State<CameraApp> createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  late CameraController controller;

  Future<void> loadModel() async {
    //Load our model
    /*
    String? res = await Tflite.loadModel(
      model: "assets/model.tflite",
      labels: "assets/labels.txt",
    );
    print(res);*/
  }

  @override
  void initState() {
    super.initState();
    loadModel();
    controller = CameraController(widget.cameras[0], ResolutionPreset.max);
    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
      controller.startImageStream((CameraImage img) {
        
        //Use our model
      });
    }).catchError((Object e) {
      if (e is CameraException) {
        switch (e.code) {
          case 'CameraAccessDenied':
            _showErrorDialog(context, 'Access Denied',
                'Camera access was denied. Please allow camera access in your device settings.');
            break;
          default:
            // Handle other errors here.
            break;
        }
      }
    });
  }

  void _showErrorDialog(BuildContext context, String title, String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: <Widget>[
            TextButton(
              child: Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Container();
    }
    return MaterialApp(
      home: SafeArea(child: CameraPreview(controller)),
    );
  }
}
