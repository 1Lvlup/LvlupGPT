import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:auto_gpt_flutter_client/views/chat/chat_input_field.dart';

// The main function is the entry point of a Flutter test file.
void main() {
  // The group function is used to group related tests together.
  group('ChatInputField tests:', () {
    // The buildTestableWidget function creates a MaterialApp widget
    // with a Scaffold to provide a consistent testing environment.
    Widget buildTestableWidget({required Widget child}) {
      return MaterialApp(
        home: Scaffold(
          body: child,
        ),
      );
    }

    // The testWidgets function is used to test Flutter widgets.
    testWidgets('renders correctly', (WidgetTester tester) async {
      // pumpWidget pumps the given Widget into the testing environment.
      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            // onSendPressed callback is provided but not used in this test.
            onSendPressed: () {},
          ),
        ),
      );

      // find.byType is used to find a widget of the given type.
      expect(find.byType(TextField), findsOneWidget); // TextField should exist
      expect(find.byIcon(Icons.send), findsOneWidget); // Send button should exist
    });

    testWidgets('text field accepts input', (WidgetTester tester) async {
      // Initialize a variable to store the entered text.
      String enteredText = '';

      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            // onSendPressed callback is not used in this test.
            onSendPressed: () {},
            // onTextChanged callback is used to store the entered text.
            onTextChanged: (text) {
              enteredText = text;
            },
          ),
        ),
      );

      // enterText is used to simulate user input in a TextField.
      await tester.enterText(find.byType(TextField), 'Hello');
      await tester.pump(); // pump is used to advance the test environment to the next frame.

      // The entered text should match the expected text.
      expect(enteredText, 'Hello');
      // The TextField should not display the entered text.
      expect(find.text('Hello'), findsNothing);
    });

    testWidgets('send button triggers callback', (WidgetTester tester) async {
      // Initialize a variable to track if the onSendPressed callback was called.
      bool onPressedCalled = false;

      await tester.pumpWidget(
        buildTestableWidget(
          child: ChatInputField(
            // onSendPressed
