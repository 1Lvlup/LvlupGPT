import 'dart:convert'; // Import the dart:convert library to work with JSON

import 'package:flutter/material.dart'; // Import the Flutter material library
import 'package:flutter_highlight/flutter_highlight.dart'; // Import the flutter\_highlight package
import 'package:flutter_highlight/themes/github.dart'; // Import the GitHub theme for flutter\_highlight
import 'package:flutter/services.dart'; // Import the Flutter services library

/// A StatefulWidget that displays a JSON string in a formatted and scrollable view.
class JsonCodeSnippetView extends StatefulWidget {
  /// The JSON string to be displayed.
  final String jsonString;

  /// Constructor for JsonCodeSnippetView.
  const JsonCodeSnippetView({
    Key? key, // The unique key for the widget.
    required this.jsonString, // The JSON string to be displayed.
  }) : super(key: key);

  @override
  _JsonCodeSnippetViewState createState() => _JsonCodeSnippetViewState();
}

/// The State class for JsonCodeSnippetView.
class _JsonCodeSnippetViewState extends State<JsonCodeSnippetView> {
  /// The decoded and formatted JSON string.
  String? prettyJson;

  /// Initialization method called when the state is created.
  @override
  void initState() {
    super.initState();
    _decodeJson(); // Decode the JSON string when the state is initialized.
  }

  /// Decodes the JSON string and sets the state with the formatted JSON.
  Future<void> _decodeJson() async {
    try {
      // Decode the JSON string and convert it to a map.
      final jsonMap = json.decode(widget.jsonString);

      // Convert the map to a formatted JSON string with indentation.
      final prettyJson = const JsonEncoder.withIndent('  ').convert(jsonMap);

      // Set the state with the formatted JSON string.
      setState(() {
        this.prettyJson = prettyJson;
      });
    } catch (e) {
      // Handle JSON decoding errors
      print('Error decoding JSON: $e');
    }
  }

  /// Builds the widget tree for the JsonCodeSnippetView.
  @override
  Widget build(BuildContext context) {
    return prettyJson == null // Check if the formatted JSON string is available
        ? const Center(child: CircularProgressIndicator()) // Display a loading indicator if the JSON string is not ready.
        : Padding(
            padding: const EdgeInsets.fromLTRB(30, 30, 0, 30), // Add padding around the JSON view.
            child: Row(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    child: HighlightView(
                      prettyJson!, // Display the formatted JSON string.
                      language: 'json', // Set the language for syntax highlighting.
                      theme: githubTheme, // Apply the GitHub theme for syntax highlighting.
                      padding: const EdgeInsets.all(12), // Add padding inside the JSON view.
                      textStyle: const TextStyle(
                        fontFamily: 'monospace', // Use a monospace font for JSON.
                        fontSize: 12, // Set the font size for JSON.
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 20), // Add some space between the JSON view and the copy button.
                Material(
                  color: Colors.white, // Use a white background for the copy button.
                  child: IconButton(
                    icon: const Icon(Icons.copy), //
