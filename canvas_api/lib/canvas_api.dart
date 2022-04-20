import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'package:flutter/material.dart';

class CanvasApiStruct {
  String canvasKey, schoolTag;
  Map<dynamic, dynamic> courses;
  CanvasApiStruct(this.canvasKey, this.schoolTag, {this.courses = const {}});

  Future<void> getCoursesWithinSixMonths() async {
    var params = {
      "per_page": 200,
      "include": ["concluded"],
      "enrollment_state": ["active"]
    };

    var baseUrl = "$schoolTag.com";
    String apiExtension = '/api/v1/courses';
    var url = Uri.https(baseUrl, apiExtension, {
      'q': '{http}',
      "Authorization": "Bearer " + canvasKey,
      "per_page": '200',
      "include": ["concluded"],
      "enrollment_state": ["active"]
    });

    var response = await http.get(url);

    if (response.statusCode == 200) {
      var r = convert.jsonDecode(response.body) as Map<String, dynamic>;
      print(r);
      courses = r;
    }
  }
}

class CanvasApiResponse extends StatefulWidget {
  const CanvasApiResponse({Key? key}) : super(key: key);

  @override
  State<CanvasApiResponse> createState() => _CanvasApiResponseState();
}

class _CanvasApiResponseState extends State<CanvasApiResponse> {
  void getCoursesWithinSixMonths(String schoolTag, String canvasKey) async {
    var baseUrl = "$schoolTag.com";
    String apiExtension = '/api/v1/courses';
    var url = Uri.https(baseUrl, apiExtension, {
      'q': '{http}',
      "Authorization": "Bearer " + canvasKey,
      "per_page": '200',
      "include": ["concluded"],
      "enrollment_state": ["active"]
    });

    var response = await http.get(url);

    if (response.statusCode == 200) {
      var r = convert.jsonDecode(response.body) as Map<String, dynamic>;
      print(r);
    }
  }

  @override
  void initState() {
    super.initState();
    getCoursesWithinSixMonths("uk",
        "1139~7U6niN8SSCYbMOze8oc8STlthT4IiRumypMKXL1UjRnmx8ACdNz8K9KrooIooFKN");
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
