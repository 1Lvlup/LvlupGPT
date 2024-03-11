import 'dart:developer';

import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/mock_data.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

class MockTaskViewModel extends TaskViewModel {
  MockTaskViewModel() : super();

  @override
  void fetchTasks() {
    tasks = mockTasks;
    notifyListeners();
  }

  @override
  void createTask(String title) {
    tasks.add(Task(id: tasks.length + 1, title: title));
    notifyListeners();
  }

  @override
  void deleteTask(int id) {
    final taskIndex = tasks.indexWhere((task) => task.id == id);
    if (taskIndex != -1) {
      tasks.removeAt(taskIndex);
      notifyListeners();
    } else {
      log('Task with id $id not found', name: 'MockTaskViewModel');
    }
  }

  @override
  void selectTask(int id) {
    final task = tasks.firstWhere((task) => task.id == id, orElse: () => null);
    if (task != null) {
      selectedTask = task;
      notifyListeners();
    } else {
      log('Task with id $id not found', name: 'MockTaskViewModel');
    }
  }
}

void main() {
  group('TaskViewModel', () {
    late TaskViewModel viewModel;

    setUp(() {
      viewModel = MockTaskViewModel();
    });

    test('Fetches tasks successfully', () {
      viewModel.fetchTasks();
      expect(viewModel.tasks, isNotEmpty);
    });

    test('Selects a task successfully', () {
      viewModel.fetchTasks();
      viewModel.selectTask(1);
      expect(viewModel.selectedTask, isNotNull);
    });

    test(
        'Notifiers are properly telling UI to update after fetching a task or selecting a task',
        () {
      bool hasNotified = false;
      viewModel.addListener(() {
        hasNotified = true;
      });

      viewModel.fetchTasks();
      expect(hasNotified, true);

      hasNotified = false; // Reset for next test
      viewModel.selectTask(1);
      expect(hasNotified, true);
    });

    test('No tasks are fetched', () {
      // Clear mock data for this test
      mockTasks.clear();

      viewModel.fetchTasks();
      expect(viewModel.tasks, isEmpty);
    });

    test('No task is selected', () {
      expect(viewModel.selectedTask, isNull);
    });

    test('Creates a task successfully', () {
      final initialCount = viewModel.tasks.length;
      viewModel.createTask('New Task');
      expect(viewModel.tasks.length, initialCount + 1);
    });

    test('Deletes a task successfully', () {
      expect(viewModel.tasks, isNotEmpty);
      final initialCount = viewModel.tasks.length;
      viewModel.deleteTask(1);
      expect(viewModel.tasks.length, initialCount - 1);
    });

    test('Deletes a task with invalid id', () {
      viewModel.fetchTasks();
      final initialCount = viewModel.tasks.length;
      viewModel.deleteTask(9999);
