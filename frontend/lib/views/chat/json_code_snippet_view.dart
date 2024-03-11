import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/github.dart';
import 'package:flutter/services.dart';

class JsonCodeSnippetView extends StatefulWidget {
  final String jsonString;

  const JsonCodeSnippetView({
    Key? key,
    required this.jsonString,
  }) : super(key: key);

  @override
  _JsonCodeSnippetViewState createState() => _JsonCodeSnippetViewState();
}

class _JsonCodeSnippetViewState extends State<JsonCodeSnippetView> {
  String? prettyJson;

  @override
  void initState() {
    super.initState();
    _decodeJson();
  }

  Future<void> _decodeJson() async {
    try {
      final jsonMap = json.decode(widget.jsonString);
      final prettyJson = const JsonEncoder.withIndent('  ').convert(jsonMap);
      setState(() {
        this.prettyJson = prettyJson;
      });
    } catch (e) {
      // Handle JSON decoding errors
      print('Error decoding JSON: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return prettyJson == null
        ? const Center(child: CircularProgressIndicator())
        : Padding(
            padding: const EdgeInsets.fromLTRB(30, 30, 0, 30),
            child: Row(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    child: HighlightView(
                      prettyJson!,
                      language: 'json',
                      theme: githubTheme,
                      padding: const EdgeInsets.all(12),
                      textStyle: const TextStyle(
                        fontFamily: 'monospace',
                        fontSize: 12,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 20),
                Material(
                  color: Colors.white,
                  child: IconButton(
                    icon: const Icon(Icons.copy),
                    onPressed: prettyJson != null
                        ? () {
                            Clipboard.setData(ClipboardData(text: prettyJson!));
                          }
                        : null,
                  ),
                ),
              ],
            ),
          );
  }
}
