import 'dart:convert';
import 'package:logging/logging.dart';

import 'package:http/http.dart' as http;
import 'package:labseries/structure.dart';

class Data {
  static Future<List<Trilogy>> data = _getData();

  static Future<List<Trilogy>> _getData() async {
    Future<http.Response> response = http.get(Uri.parse('https://trilogy-server.azurewebsites.net/trilogies'));

    return response.then((response) {
      if (response.statusCode != 200) {
        Logger.root.log(Level.WARNING, response.body);
        throw Exception('Data could not be loaded, error code: ${response.statusCode}.');
      }

      return (json.decode(response.body) as List)
        .cast<Map<String, dynamic>>()
        .map(Trilogy.fromJson)
        .toList();
    });
  }
}