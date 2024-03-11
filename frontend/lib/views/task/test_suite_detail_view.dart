import 'package:flutter/material.dart';

class TaskListTile extends StatelessWidget {
  final Task task;
  final VoidCallback onTap;
  final VoidCallback onDelete;
  final bool selected;

  const TaskListTile({
    Key? key,
    required this.task,
    required this.onTap,
    required this.onDelete,
    this.selected = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Checkbox(
        value: selected,
        onChanged: (_) {},
      ),
      title: Text(task.title),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          IconButton(
            icon: Icon(Icons.edit),
            onPressed: onTap,
          ),
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: onDelete,
          ),
        ],
      ),
    );
  }
}


import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TestSuiteDetailView extends StatefulWidget {
  final TaskViewModel viewModel;
  final TestSuite testSuite;

  const TestSuiteDetailView({
    Key? key,
    required this.testSuite,
    required this.viewModel,
  }) : super(key: key);

  @override
  _TestSuiteDetailViewState createState() => _TestSuiteDetailViewState();
}

class _TestSuiteDetailViewState extends State<TestSuiteDetailView> {
  late ChatViewModel _chatViewModel;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _chatViewModel = Provider.of<ChatViewModel>(context, listen: false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.grey,
        foregroundColor: Colors.black,
        title: Text("${widget.testSuite.timestamp}"),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () => widget.viewModel.deselectTestSuite(),
        ),
      ),
      body: Column(
        children: [
          // Task List
          Expanded(
            child: ListView.builder(
              itemCount: widget.testSuite.tests.length,
              itemBuilder: (context, index) {
                final task = widget.testSuite.tests[index];
                return TaskListTile(
                  task: task,
                  onTap: () {
                    widget.viewModel.selectTask(task.id);
                    _chatViewModel.setCurrentTaskId(task.id);
                    print('Task ${task.title} tapped');
                  },
                  onDelete: () {
                    widget.viewModel.deleteTask(task.id);
                    if (_chatViewModel.currentTaskId == task.id) {
                      _chatViewModel.clearCurrentTaskAndChats();
                    }
                    print('Task ${task.title} delete button tapped');
                  },
                  selected: task.id == widget.viewModel.selectedTask?.id,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
