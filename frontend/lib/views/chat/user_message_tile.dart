import 'package:flutter/material.dart';

class UserMessageTile extends StatelessWidget {
  final String message;

  const UserMessageTile({
    Key? key,
    required this.message,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        double chatViewWidth = constraints.maxWidth;
        double tileWidth = (chatViewWidth >= 1000) ? 900 : chatViewWidth - 40;

        return Align(
          alignment: Alignment.centerRight, // Align user messages to the right
          child: Container(
            width: tileWidth,
            constraints: const BoxConstraints(
              minHeight: 50,
            ),
            margin: const EdgeInsets.symmetric(vertical: 8),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
            decoration: BoxDecoration(
              color: Colors.blue.shade200, // User message background color
              borderRadius: BorderRadius.circular(4),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.end, // Align message to the right
              children: [
                Expanded(
                  child: SelectableText(
                    message,
                    maxLines: null,
                    style: const TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
