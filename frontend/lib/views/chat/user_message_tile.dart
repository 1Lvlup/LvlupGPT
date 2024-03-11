import 'package:flutter/material.dart';

/// A widget displaying a user message in a chat interface.
///
/// The message is right-aligned with a blue background and adjusts its width
/// based on the available chat view width.
class UserMessageTile extends StatelessWidget {
  /// The message to display in the user message tile.
  final String message;

  /// Constructs a UserMessageTile widget with the given message.
  const UserMessageTile({
    Key? key,
    required this.message,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        /// Calculates the width for the chat view and user message tile.
        double chatViewWidth = constraints.maxWidth;
        double tileWidth = (chatViewWidth >= 1000) ? 900 : chatViewWidth - 40;

        return Align(
          /// Aligns user messages to the right side of the chat interface.
          alignment: Alignment.centerRight,
          child: Container(
            /// Sets the width of the user message tile.
            width: tileWidth,

            /// Configures minimum height for the user message tile.
            constraints: const BoxConstraints(
              minHeight: 50,
            ),

            /// Adds margin around the user message tile.
            margin: const EdgeInsets.symmetric(vertical: 8),

            /// Adds padding inside the user message tile.
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),

            /// Applies a blue background color to the user message tile.
            decoration: BoxDecoration(
              color: Colors.blue.shade200,
              borderRadius: BorderRadius.circular(4),
            ),

            /// Displays the user message within the tile.
            child: Row(
              /// Aligns the message to the right side of the tile.
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Expanded(
                  /// Displays the message text, allowing user selection.
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
