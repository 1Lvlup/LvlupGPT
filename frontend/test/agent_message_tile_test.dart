import 'package:auto_gpt_flutter_client/views/chat/agent_message_tile.dart';
import 'package:auto_gpt_flutter_client/views/chat/json_code_snippet_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  // The main function is the entry point of the test suite. It contains a list of
  // test cases to be executed.

  // Test to verify that the AgentMessageTile renders correctly
  testWidgets('Renders AgentMessageTile', (WidgetTester tester) async {
    // Set up the test environment by pumping a MaterialApp widget with a
    // Scaffold that contains an AgentMessageTile widget.
    await tester.pumpWidget(const MaterialApp(
      home: Scaffold(
        body: AgentMessageTile(message: 'Test Message'),
      ),
    ));

    // Verify that the agent title is displayed.
    expect(find.text('Agent'), findsOneWidget);

    // Verify that the message text is displayed.
    expect(find.text('Test Message'), findsOneWidget);
  });

  // Test to verify that the expand/collapse functionality works
  testWidgets('Toggle Expand/Collapse', (WidgetTester tester) async {
    // Set up the test environment by pumping a MaterialApp widget with a
    // Scaffold that contains an AgentMessageTile widget.
    await tester.pumpWidget(const MaterialApp(
      home: Scaffold(
        body: AgentMessageTile(message: 'Test Message'),
      ),
    ));

    // Verify that the JSON code snippet is not visible initially.
    expect(find.byType(JsonCodeSnippetView), findsNothing);

    // Tap the expand/collapse button to show the JSON code snippet.
    await tester.tap(find.byIcon(Icons.keyboard_arrow_down));
    await tester.pumpAndSettle();

    // Verify that the JSON code snippet is now visible.
    expect(find.byType(JsonCodeSnippetView), findsOneWidget);

    // Tap the expand/collapse button again to hide the JSON code snippet.
    await tester.tap(find.byIcon(Icons.keyboard_arrow_up));
    await tester.pumpAndSettle();

    // Verify that the JSON code snippet is hidden again.
    expect(find.byType(JsonCodeSnippetView), findsNothing);
  });
}

