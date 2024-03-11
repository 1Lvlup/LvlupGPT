import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:auto_gpt_flutter_client/views/chat/chat_input_field.dart';

void main() {
  group('ChatInputField tests:', () {
    Widget buildTestableWidget({required Widget child}) {
      return MaterialApp(
        home: Scaffold(
          body: child,
        ),
      );
    }

    testWidgets('renders correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            onSendPressed: () {},
          ),
        ),
      );

      expect(find.byType(TextField), findsOneWidget);
      expect(find.byIcon(Icons.send), findsOneWidget);
    });

    testWidgets('text field accepts input', (WidgetTester tester) async {
      String enteredText = '';

      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            onSendPressed: () {},
            onTextChanged: (text) {
              enteredText = text;
            },
          ),
        ),
      );

      await tester.enterText(find.byType(TextField), 'Hello');
      await tester.pump();

      expect(enteredText, 'Hello');
      expect(find.text('Hello'), findsNothing); // TextField should not display input
    });

    testWidgets('send button triggers callback', (WidgetTester tester) async {
      bool onPressedCalled = false;

      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            onSendPressed: () {
              onPressedCalled = true;
            },
          ),
        ),
      );

      await tester.tap(find.byIcon(Icons.send));
      await tester.pump();

      expect(onPressedCalled, isTrue);
    });
  });
}
