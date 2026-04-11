import 'package:flutter/material.dart';
import 'package:labseries/data.dart';
import 'package:labseries/list_page.dart';
import 'package:logging/logging.dart';

void main() {
  Logger.root.level = Level.FINE; // ALL; defaults to Level.INFO (https://pub.dev/packages/logging)
  Logger.root.onRecord.listen((record) {
    debugPrint('${record.loggerName}: ${record.level.name}: ${record.time}: ${record.message}');
  });
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    ColorScheme colorScheme = ColorScheme.fromSeed(seedColor: Colors.green);
    return MaterialApp(
      theme: ThemeData(
        colorScheme: colorScheme,
        appBarTheme: AppBarTheme(
          backgroundColor: colorScheme.primaryContainer,
        ),
        bottomNavigationBarTheme: BottomNavigationBarThemeData(
          backgroundColor: colorScheme.primaryContainer,
        )
      ),
      home: ListPage(Data.data)
    );
  }
}
