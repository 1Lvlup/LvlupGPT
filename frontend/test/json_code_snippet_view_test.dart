import 'package:auto_gpt_flutter_client/views/chat/json_code_snippet_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const String jsonString = '{"key": "value"}';

  group('JsonCodeSnippetView tests:', () {
    testWidgets('renders without crashing', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: JsonCodeSnippetView(jsonString: jsonString),
          ),
        ),
      );

      expect(find.byType(JsonCodeSnippetView), findsOneWidget);
    });

    testWidgets('displays the JSON string correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: JsonCodeSnippetView(jsonString: jsonString),
          ),
        ),
      );

      expect(find.text('"key": "value"'), findsOneWidget);
    });
  });
}
