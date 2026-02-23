import 'package:flutter/material.dart';
import 'package:labseries/data.dart';
import 'package:labseries/detailed_page.dart';

    void main() {
      runApp(const MainApp());
    }

    class MainApp extends StatelessWidget {
      const MainApp({super.key});

      @override
      Widget build(BuildContext context) {
        return const MaterialApp(
          home: DetailedPage(data),
        );
      }
    }