import 'package:auto_gpt_flutter_client/services/prefs_service.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_input_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

/// A custom [StatelessWidget] for the chat input field.
///
/// This widget displays a scrollable text field with a send button and a
/// continuous mode button. The text field is connected to a [ChatInputViewModel]
/// to handle user input and sending messages.
class ChatInputField extends StatelessWidget {
  const ChatInputField({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    /// Accesses the [ChatInputViewModel] instance in the widget's build context.
    final chatInputViewModel = context.watch<ChatInputViewModel>();

    /// The [LayoutBuilder] is used to determine the available width for the input field
    /// and adjust it accordingly.
    return LayoutBuilder(
      builder: (context, constraints) {
        double inputWidth = (constraints.maxWidth >= 1000) ? 900 : constraints.maxWidth - 40;

        return Container(
          /// The input field's width is set based on the available width.
          width: inputWidth,
          constraints: const BoxConstraints(
            minHeight: 50,
            maxHeight: 400,
          ),
          /// The input field's decoration includes a border, border radius, and background color.
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: Colors.black, width: 0.5),
            borderRadius: BorderRadius.circular(8),
          ),
          /// Padding is added to the input field for better user experience.
          padding: const EdgeInsets.symmetric(horizontal: 8),
          child: SingleChildScrollView(
            reverse: true,
            child: TextField(
              /// Connects the text field to the [ChatInputViewModel]'s text controller.
              controller: chatInputViewModel.textController,
              /// Connects the text field to the [ChatInputViewModel]'s focus node.
              focusNode: chatInputViewModel.focusNode,
              /// Calls the [ChatInputViewModel]'s onSendPressed method when the text field's form is submitted.
              onSubmitted: (_) {
                chatInputViewModel.onSendPressed();
              },
              /// Allows the text field to have multiple lines and grow as needed.
              maxLines: null,
              /// The input field's decoration includes a hint text and hides the default border.
              decoration: InputDecoration(
                hintText: 'Type a message...',
                border: InputBorder.none,
                /// The suffix icon includes a send button and a continuous mode button.
                suffixIcon: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    /// The send button is disabled when the continuous mode is active.
                    IconButton(
                      splashRadius: 0.1,
                      icon: const Icon(Icons.send),
                      onPressed: chatInputViewModel.isContinuousMode
                          ? null
                          : () {
                              chatInputViewModel.onSendPressed();
                            },
                    ),
                    /// The continuous mode button toggles the continuous mode.
                    IconButton(
                      splashRadius: 0.1,
                      icon: Icon(chatInputViewModel.isContinuousMode
                          ? Icons.pause
                          : Icons.fast_forward),
                      onPressed: () {
                        chatInputViewModel.toggleContinuousMode();
                      },
                    )
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}

/// A view model for handling chat input functionality.
class ChatInputViewModel extends ChangeNotifier {
  /// Creates a new instance of the [ChatInputViewModel] class.
  ChatInputViewModel({
    required this.prefsService,
  }) : super() {
    /// Sets up a listener for the focus node to toggle the continuous mode when the text field loses focus.
    _focusNode.addListener(() {
      if (_focusNode.hasFocus && isContinuousMode) {
        toggleContinuousMode();
      }
    });
  }

  /// The [PrefsService] instance for storing and retrieving user preferences.
  final PrefsService prefsService;

  /// The text controller for managing the text input in the chat input field.
  final TextEditingController textController = TextEditingController();

  /// The focus node for managing the focus state of the chat input field.
  final FocusNode _focusNode = FocusNode();

  /// A flag indicating whether the continuous mode is active.
  bool isContinuousMode = false;

  /// Called when the user presses the send button or submits the text field form.
  void onSendPressed() {
    if (textController.text.isNotEmpty) {
      /// Checks if the user prefers to see the continuous mode dialog.
      final showContinuousModeDialog = prefsService.getBool('showContinuousModeDialog') ?? true;

      if (!showContinuousModeDialog) {
        /// Sends the message without showing the dialog.
        _executeSendMessage();
      } else {
        /// Shows the continuous mode dialog and sends the message if the user proceeds.
        prefsService.setBool('showContinuousModeDialog', false);
        showDialog(
          context: navigatorKey.currentContext!,
          builder: (BuildContext context) {
            return ContinuousModeDialog(
              onProceed: () {
                Navigator.of(context).pop();
                _executeSendMessage();
              },
            );
          },
        );
      }
    }
  }

  /// Toggles the continuous mode between active and inactive states.
  void toggleContinuousMode() {
    isContinuousMode =
