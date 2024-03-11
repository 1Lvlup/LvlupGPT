import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:flutter/material.dart';

/// A custom list tile for displaying a TestSuite.
/// When the user taps on the list tile, the onTap callback is called.
class TestSuiteListTile extends StatelessWidget {
  /// The TestSuite to display in the list tile.
  final TestSuite testSuite;

  /// The callback function to be called when the user taps on the list tile.
  final VoidCallback onTap;

  /// Constructor for TestSuiteListTile.
  const TestSuiteListTile({
    Key? key,
    required this.testSuite, // Required: the TestSuite to display
    required this.onTap, // Required: the callback function
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    /// Calculate the width of the list tile based on the available width.
    final double tileWidth = MediaQuery.of(context).size.width - 32;

    return GestureDetector(
      onTap: onTap,
      child: Card(
        /// Add margin around the list tile.
        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        clipBehavior: Clip.hardEdge,
        /// Round the corners of the list tile.
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        child: InkWell(
          onTap: onTap,
          /// Round the corners of the InkWell to match the Card.
          borderRadius: BorderRadius.circular(8),
          splashColor: Colors.blue.withAlpha(30),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 16),
            child: Row(
              children: [
                /// Play arrow icon.
                const Icon(Icons.play_arrow, color: Colors.black),
                const SizedBox(width: 12),
                /// Display the testSuite's timestamp.
                Expanded(
                  child: Text(
                    testSuite.timestamp,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: Colors.black),
                  ),
                ),
                /// Chevron right icon.
                const Icon(Icons.chevron_right, color: Colors.
