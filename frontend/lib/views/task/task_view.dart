import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/task/test_suite_detail_view.dart';
import 'package:auto_gpt_flutter_client/views/task/test_suite_list_tile.dart';
import 'package:flutter/material.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/task/new_task_button.dart';
import 'package:auto_gpt_flutter_client/views/task/task_list_tile.dart';
import 'package:provider/provider.dart';

class TaskView extends StatelessWidget {
  final TaskViewModel viewModel;

  const TaskView({Key? key, required this.viewModel}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          Column(
            children: [
              // Title and New Task button
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: NewTaskButton(
                  onPressed: () {
                    final chatViewModel = context.watch<ChatViewModel>();
                    chatViewModel.clearCurrentTaskAndChats();
                    viewModel.deselectTask();
                  },
                ),
              ),
              // Task List
              Expanded(
                child: Consumer<SettingsViewModel>(
                  builder: (context, settingsViewModel, child) {
                    final isDeveloperModeEnabled =
                        settingsViewModel.isDeveloperModeEnabled;
                    return ListView.separated(
                      itemCount: viewModel.combinedDataSource.length,
                      separatorBuilder: (context, index) => const Divider(),
                      itemBuilder: (context, index) {
                        final item = viewModel.combinedDataSource[index];

                        if (item is Task) {
                          return TaskListTile(
                            task: item,
                            onTap: () {
                              viewModel.selectTask(item.id);
                              final chatViewModel = context.watch<ChatViewModel>();
                              chatViewModel.setCurrentTaskId(item.id);
                            },
                            onDelete: () {
                              viewModel.deleteTask(item.id);
                              if (chatViewModel.currentTaskId == item.id) {
                                chatViewModel.clearCurrentTaskAndChats();
                              }
                            },
                            selected: item.id == viewModel.selectedTask?.id,
                          );
                        } else if (item is TestSuite) {
                          return TestSuiteListTile(
                            testSuite: item,
                            onTap: () {
                              viewModel.deselectTask();
                              viewModel.selectTestSuite(item);
                              context.watch<ChatViewModel>().clearCurrentTaskAndChats();
                            },
                          );
                        } else {
                          return const SizedBox.shrink();
                        }
                      },
                    );
                  },
                ),
              ),
            ],
          ),
          if (viewModel.selectedTestSuite != null)
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              child: TestSuiteDetailView(
                testSuite: viewModel.selectedTestSuite!,
                viewModel: viewModel,
              ),
            ),
        ],
      ),
    );
  }
}
