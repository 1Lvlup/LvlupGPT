import 'package:auto_gpt_flutter_client/models/task.dart'; // Import Task model
import 'package:auto_gpt_flutter_client/models/test_suite.dart'; // Import TestSuite model
import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart'; // Import SettingsViewModel
import 'package:auto_gpt_flutter_client/views/task/test_suite_detail_view.dart'; // Import TestSuiteDetailView
import 'package:auto_gpt_flutter_client/views/task/test_suite_list_tile.dart'; // Import TestSuiteListTile
import 'package:flutter/material.dart'; // Import Material Design widgets
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart'; // Import TaskViewModel
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart'; // Import ChatViewModel
import 'package:auto_gpt_flutter_client/views/task/new_task_button.dart'; // Import NewTaskButton
import 'package:auto_gpt_flutter_client/views/task/task_list_tile.dart'; // Import TaskListTile
import 'package:provider/provider.dart'; // Import Provider package

// TaskView is a StatelessWidget that displays a list of tasks and test suites
class TaskView extends StatelessWidget {
  final TaskViewModel viewModel; // TaskViewModel instance

  const TaskView({Key? key, required this.viewModel}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold( // Create a Scaffold widget, which is a basic Material Design screen structure
      backgroundColor: Colors.white, // Set background color to white
      body: Stack( // Use Stack to overlay the TestSuiteDetailView on top of the TaskView
        children: [
          Column( // Column to hold the title, new task button, and task list
            children: [
              // Title and New Task button
              Padding(
                padding: const EdgeInsets.all(8.0), // Add padding around the NewTaskButton
                child: NewTaskButton( // NewTaskButton widget
                  onPressed: () { // Callback when the NewTaskButton is pressed
                    final chatViewModel = context.watch<ChatViewModel>(); // Get the ChatViewModel instance
                    chatViewModel.clearCurrentTaskAndChats(); // Clear the current task and chats
                    viewModel.deselectTask(); // Deselect the currently selected task
                  },
                ),
              ),
              // Task List
              Expanded( // Expanded widget to fill the available space with the task list
                child: Consumer<SettingsViewModel>( // Consumer to listen to SettingsViewModel changes
                  builder: (context, settingsViewModel, child) {
                    final isDeveloperModeEnabled = // Get the developer mode status from SettingsViewModel
                        settingsViewModel.isDeveloperModeEnabled;
                    return ListView.separated( // ListView to display the tasks and test suites
                      itemCount: viewModel.combinedDataSource.length, // Number of items in the list
                      separatorBuilder: (context, index) => const Divider(), // Divider between list items
                      itemBuilder: (context, index) {
                        final item = viewModel.combinedDataSource[index]; // Get the current item

                        if (item is Task) { // If the item is a Task
                          return TaskListTile( // Display a TaskListTile
                            task: item, // Pass the Task instance
                            onTap: () { // Callback when the TaskListTile is tapped
                              viewModel.selectTask(item.id); // Select the task
                              final chatViewModel = context.watch<ChatViewModel>(); // Get the ChatViewModel instance
                              chatViewModel.setCurrentTaskId(item.id); // Set the current task ID
                            },
                            onDelete: () { // Callback when the TaskListTile delete button is pressed
                              viewModel.deleteTask(item.id); // Delete the task
                              if (chatViewModel.currentTaskId == item.id) {
                                chatViewModel.clearCurrentTaskAndChats(); // Clear the current task and chats
                              }
                            },
                            selected: item.id == viewModel.selectedTask?.id, // Set the selected state
                          );
                        } else if (item is TestSuite) { // If the item is a TestSuite
                          return TestSuiteListTile( // Display a TestSuiteListTile
                            testSuite: item, // Pass the TestSuite instance
                            onTap: () { // Callback when the TestSuiteListTile is tapped
                              viewModel.deselectTask(); // Deselect the currently selected task
                              viewModel.selectTestSuite(item); // Select the test suite
                              context.watch<ChatViewModel>().clearCurrentTaskAndChats(); // Clear the current task and chats
                            },
                          );
                        } else {
                          return const SizedBox.shrink(); // Return an empty SizedBox if the item is neither a Task nor a TestSuite
                        }
                      },
                    );
                  },
                ),
              ),
            ],
          ),
          if (viewModel.selectedTestSuite != null) // If a test suite is selected
            Positioned( // Position the TestSuiteDetailView on top of the TaskView
              top: 0, // Align the top edge of the TestSuiteDetailView with the top edge of the TaskView
              left: 0, // Align the left edge of the TestSuiteDetailView with the left edge of the TaskView
              right: 0, // Align the right edge of the TestSuiteDetailView with the right edge of the TaskView
              bottom: 0, // Align the bottom edge of the TestSuiteDetailView with the bottom edge of the TaskView
              child: TestSuiteDetailView( // TestSuiteDetailView widget
                testSuite: viewModel.selectedTestSuite!, // Pass the selected TestSuite instance
                viewModel: viewModel, // Pass the TaskViewModel instance
              ),
            ),

