import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart'; // This import is duplicated
import 'package:auto_gpt_flutter_client/viewmodels/skill_tree_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/settings/settings_view.dart';
import 'package:auto_gpt_flutter_client/views/side_bar/side_bar_view.dart';
import 'package:auto_gpt_flutter_client/views/skill_tree/skill_tree_view.dart';
import 'package:auto_gpt_flutter_client/views/task/task_view.dart';
import 'package:auto_gpt_flutter_client/views/chat/chat_view.dart';
import 'package:auto_gpt_flutter_client/views/task_queue/task_queue_view.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// MainLayout is a StatelessWidget, meaning it doesn't store any mutable state.
class MainLayout extends StatelessWidget {
  // A ValueNotifier holds a value that can be listened to by other objects.
  final ValueNotifier<String> selectedViewNotifier = ValueNotifier('TaskView');

  MainLayout({super.key});

  // The build method returns a Widget that represents the layout of this app.
  @override
  Widget build(BuildContext context) {
    // The width of the screen.
    double width = MediaQuery.of(context).size.width;

    // The width of the sidebar.
    double sideBarWidth = 60.0;

    // The remaining width after subtracting the sidebar width.
    double remainingWidth = width - sideBarWidth;

    // A function that calculates the widths of the different views based on the remaining width.
    _calculateViewWidths(double remainingWidth) {
      double taskViewWidth = 280.0;
      double settingsViewWidth = 280.0;
      double skillTreeViewWidth = 0;
      double testQueueViewWidth = 0;
      double chatViewWidth = 0;

      // If the width is greater than 800, then we can split the screen into multiple views.
      if (width > 800) {
        if (selectedViewNotifier.value == 'TaskView') {
          // If the selected view is the task view, then we split the remaining width between the skill tree view and the chat view.
          chatViewWidth = remainingWidth - taskViewWidth;
          skillTreeViewWidth = taskViewWidth;
          testQueueViewWidth = 0;
        } else if (selectedViewNotifier.value == 'SettingsView') {
          // If the selected view is the settings view, then we split the remaining width between the settings view and the chat view.
          chatViewWidth = remainingWidth - settingsViewWidth;
          skillTreeViewWidth = settingsViewWidth;
          testQueueViewWidth = 0;
        } else {
          // If the selected view is neither the task view nor the settings view, then we adjust the widths based on the selected node in the skill tree view.
          if (Provider.of<SkillTreeViewModel>(context, listen: false).selectedNode != null) {
            skillTreeViewWidth = remainingWidth * 0.25;
            testQueueViewWidth = remainingWidth * 0.25;
            chatViewWidth = remainingWidth * 0.5;
          } else {
            skillTreeViewWidth = remainingWidth * 0.5;
            chatViewWidth = remainingWidth * 0.5;
            testQueueViewWidth = 0;
          }
        }
      }

      // Return the calculated widths as a list.
      return [skillTreeViewWidth, testQueueViewWidth, chatViewWidth];
    }

    // Call the _calculateViewWidths function with the remaining width as an argument.
    double[] viewWidths = _calculateViewWidths(remainingWidth);
    double skillTreeViewWidth = viewWidths[0];
    double testQueueViewWidth = viewWidths[1];
    double chatViewWidth = viewWidths[2];

    // Get the instances of the TaskViewModel, ChatViewModel, and SettingsViewModel.
    final taskViewModel = Provider.of<TaskViewModel>(context);
    final chatViewModel = Provider.of<ChatViewModel>(context);
    final settings
