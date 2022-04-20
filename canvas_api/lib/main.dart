import 'package:flutter/material.dart';
import 'canvas_api.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const CanvasApi(),
    );
  }
}

class CanvasApi extends StatefulWidget {
  const CanvasApi({Key? key}) : super(key: key);

  @override
  State<CanvasApi> createState() => _CanvasApiState();
}

class _CanvasApiState extends State<CanvasApi> {
  final TextEditingController myController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Canvas API")),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(32.0),
            child: TextField(
              autofocus: true,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Enter Canvas API Key',
              ),
              // onSubmitted: _newCanvasCall,
              controller: myController,
            ),
          ),
          const CanvasApiResponse()
        ],
      ),
    );
  }
}
