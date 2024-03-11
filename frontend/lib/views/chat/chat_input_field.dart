import 'package:auto_gpt_flutter_client/services/prefs_service.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_input_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ChatInputField extends StatelessWidget {
  const ChatInputField({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final chatInputViewModel = context.watch<ChatInputViewModel>();

    return LayoutBuilder(
      builder: (context, constraints) {
        double inputWidth = (constraints.maxWidth >= 1000) ? 900 : constraints.maxWidth - 40;

        return Container(
          width: inputWidth,
          constraints: const BoxConstraints(
            minHeight: 50,
            maxHeight: 400,
          ),
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: Colors.black, width: 0.5),
            borderRadius: BorderRadius.circular(8),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 8),
          child: SingleChildScrollView(
            reverse: true,
            child: TextField(
              controller: chatInputViewModel.textController,
              focusNode: chatInputViewModel.focusNode,
              onSubmitted: (_) {
                chatInputViewModel.onSendPressed();
              },
              maxLines: null,
              decoration: InputDecoration(
                hintText: 'Type a message...',
                border: InputBorder.none,
                suffixIcon: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      splashRadius: 0.1,
                      icon: const Icon(Icons.send),
                      onPressed: chatInputViewModel.isContinuousMode
                          ? null
                          : () {
                              chatInputViewModel.onSendPressed();
                            },
                    ),
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

class ChatInputViewModel extends ChangeNotifier {
  ChatInputViewModel({
    required this.prefsService,
  }) : super() {
    _focusNode.addListener(() {
      if (_focusNode.hasFocus && isContinuousMode) {
        toggleContinuousMode();
      }
    });
  }

  final PrefsService prefsService;
  final TextEditingController textController = TextEditingController();
  final FocusNode _focusNode = FocusNode();

  bool isContinuousMode = false;

  void onSendPressed() {
    if (textController.text.isNotEmpty) {
      final showContinuousModeDialog = prefsService.getBool('showContinuousModeDialog') ?? true;

      if (!showContinuousModeDialog) {
        _executeSendMessage();
      } else {
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

  void toggleContinuousMode() {
    isContinuousMode = !isContinuousMode;
    notifyListeners();

    if (isContinuousMode) {
      _executeContinuousMode();
    } else {
      textController.clear();
    }
  }

  void _executeSendMessage() {
    // Implement sending the message here
  }

  void _executeContinuousMode() {
    // Implement continuous mode here
  }

  @override
  void dispose() {
    textController.dispose();
    _focusNode.dispose();
    super.dispose();
  }
}
