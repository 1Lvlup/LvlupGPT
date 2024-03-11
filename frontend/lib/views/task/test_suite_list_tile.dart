import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:flutter/material.dart';

class TestSuiteListTile extends StatelessWidget {
  final TestSuite testSuite;
  final VoidCallback onTap;

  const TestSuiteListTile({
    Key? key,
    required this.testSuite,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final double tileWidth = MediaQuery.of(context).size.width - 32;

    return GestureDetector(
      onTap: onTap,
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        clipBehavior: Clip.hardEdge,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(8),
          splashColor: Colors.blue.withAlpha(30),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 16),
            child: Row(
              children: [
                const Icon(Icons.play_arrow, color: Colors.black),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    testSuite.timestamp,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: Colors.black),
                  ),
                ),
                const Icon(Icons.chevron_right, color: Colors.grey),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
