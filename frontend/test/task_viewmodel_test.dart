import 'dart:developer';

// Importing necessary packages for testing and mocking.
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/mock_data.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

// Defining a mock class for TaskViewModel to override its methods for testing.
class MockTaskViewModel extends TaskViewModel {
  MockTaskViewModel() : super();

  // Overriding fetchTasks method to use mockTasks instead of making actual API calls.
  @override
  void fetchTasks() {
    tasks = mockTasks;
    notifyListeners();
  }

  // Overriding createTask method to directly add a task to the tasks list.
  @override
  void createTask(String title) {
    tasks.add(Task(id: tasks.length + 1, title: title));
    notifyListeners();
  }

  // Overriding deleteTask method to check for task existence before deletion.
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

  // Overriding selectTask method to check for task existence before selection.
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
  // Defining a group for TaskViewModel tests.
  group('TaskViewModel', () {
    late TaskViewModel viewModel;

    // Setting up the test environment by creating a new instance of MockTaskViewModel.
    setUp(() {
      viewModel = MockTaskViewModel();
    });

    // Testing if tasks are fetched successfully.
    test('Fetches tasks successfully', () {
      viewModel.fetchTasks();
      expect(viewModel.tasks, isNotEmpty);
    });

    // Testing if a task is selected successfully.
    test('Selects a task successfully', () {
      viewModel.fetchTasks();
      viewModel.selectTask(1);
      expect(viewModel.selectedTask, isNotNull);
    });

    // Testing if notifiers are properly telling UI to update after fetching a task or selecting a task.
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

    // Testing if no tasks are fetched when the mockTasks list is empty.
    test('No tasks are fetched', () {
      // Clear mock data for this test
      mockTasks.clear();

      viewModel.fetchTasks();
      expect(viewModel.tasks, isEmpty);
    });

    // Testing if no task is selected when there are no tasks.
    test('No task is selected', () {
      expect(viewModel.selectedTask, isNull);
    });

    // Testing if a task is created successfully.
    test('Creates a task successfully', () {
      final initialCount = viewModel.tasks.length;
      viewModel.createTask('New Task');
      expect(viewModel.tasks.length, initialCount + 1);
    });

    // Testing if a task is deleted successfully.
    test('Deletes a task successfully', () {
      expect(viewModel.tasks, isNotEmpty);
      final initialCount = viewModel.tasks.length;
      viewModel.deleteTask(1);
      expect(viewModel.tasks.length, initialCount - 1);
    });

    // Testing if a task with an invalid id is deleted.
    test('Deletes a task with invalid id', () {
      viewModel.fetchTasks();
      final initialCount = viewModel.tasks.length;
