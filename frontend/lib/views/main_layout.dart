import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
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

class MainLayout extends StatelessWidget {
  final ValueNotifier<String> selectedViewNotifier = ValueNotifier('TaskView');

  MainLayout({super.key});

  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width;

    double sideBarWidth = 60.0;
    double remainingWidth = width - sideBarWidth;

    _calculateViewWidths(double remainingWidth) {
      double taskViewWidth = 280.0;
      double settingsViewWidth = 280.0;
      double skillTreeViewWidth = 0;
      double testQueueViewWidth = 0;
      double chatViewWidth = 0;

      if (width > 800) {
        if (selectedViewNotifier.value == 'TaskView') {
          chatViewWidth = remainingWidth - taskViewWidth;
          skillTreeViewWidth = taskViewWidth;
          testQueueViewWidth = 0;
        } else if (selectedViewNotifier.value == 'SettingsView') {
          chatViewWidth = remainingWidth - settingsViewWidth;
          skillTreeViewWidth = settingsViewWidth;
          testQueueViewWidth = 0;
        } else {
          if (Provider.of<SkillTreeViewModel>(context, listen: false)
                  .selectedNode !=
              null) {
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

      return (skillTreeViewWidth, testQueueViewWidth, chatViewWidth);
    }

    double[] viewWidths = _calculateViewWidths(remainingWidth);
    double skillTreeViewWidth = viewWidths[0];
    double testQueueViewWidth = viewWidths[1];
    double chatViewWidth = viewWidths[2];

    final taskViewModel = Provider.of<TaskViewModel>(context);
    final chatViewModel = Provider.of<ChatViewModel>(context);
    final settingsViewModel = Provider.of<SettingsViewModel>(context);

    return width > 800;
