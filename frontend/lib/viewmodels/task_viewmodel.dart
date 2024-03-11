import 'dart:convert';

// Importing necessary packages and models for handling tasks and test suites.
import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/test_suite.dart';

// Importing services for handling shared preferences and tasks.
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/services/task_service.dart';

// Importing Flutter's foundation for ChangeNotifier.
import 'package:flutter/foundation.dart';

// Importing collection for collection utilities.
import 'package:collection/collection.dart';

// TaskViewModel is a class that manages tasks and test suites, providing
// methods for creating, deleting, fetching, and selecting tasks and test suites.
class TaskViewModel with ChangeNotifier {
  // Dependency injection for TaskService and SharedPreferencesService.
  final TaskService _taskService;
  final SharedPreferencesService _prefsService;

  // Private properties for storing tasks and test suites.
  List<Task> _tasks = [];
  List<TestSuite> _testSuites = [];

  // Additional data sources for tasks and test suites, possibly for UI purposes.
  List<Task> _tasksDataSource = [];
  List<TestSuite> _testSuitesDataSource = [];

  // SelectedTask and SelectedTestSuite properties for tracking the currently
  // selected task and test suite.
  Task? _selectedTask;
  TestSuite? _selectedTestSuite;

  // A flag indicating whether the view model is waiting for an agent response.
  bool _isWaitingForAgentResponse = false;

  // Getter for isWaitingForAgentResponse.
  bool get isWaitingForAgentResponse => _isWaitingForAgentResponse;

  // TaskViewModel constructor, initializing the TaskService and
  // SharedPreferencesService dependencies.
  TaskViewModel(this._taskService, this._prefsService);

  // Getters for selectedTask and selectedTestSuite.
  Task? get selectedTask => _selectedTask;
  TestSuite? get selectedTestSuite => _selectedTestSuite;

  // createTask method for creating a new task with the given title and notifying
  // listeners about the changes.
  Future<String> createTask(String title) async {
    _isWaitingForAgentResponse = true;
    notifyListeners();

    try {
      // Preparing the newTaskRequestBody and calling the createTask method
      // from the TaskService.
      final newTaskRequestBody = TaskRequestBody(input: title);
      final createdTask = await _taskService.createTask(newTaskRequestBody);

      // Creating a new Task object from the created task response and adding
      // it to the tasks and tasksDataSource lists.
      final newTaskObject =
          Task(id: createdTask['task_id'], title: createdTask['input']);
      _tasks.add(newTaskObject);
      _tasksDataSource.add(newTaskObject);

      // Reversing the tasks list to display the latest task at the top.
      _tasks = _tasks.reversed.toList();

      notifyListeners();

      // Returning the new task's ID.
      final taskId = newTaskObject.id;
      print("Task $taskId created successfully!");

      return newTaskObject.id;
    } catch (e, stackTrace) {
      print('Error creating task: $e\n$stackTrace');
      rethrow;
    } finally {
      _isWaitingForAgentResponse = false;
      notifyListeners();
    }
  }

  // deleteTask method for deleting a task with the given taskId and notifying
  // listeners about the changes.
  void deleteTask(String taskId) {
    _taskService.saveDeletedTask(taskId);
    _tasks.removeWhere((task) => task.id == taskId);
    _tasksDataSource.removeWhere((task) => task.id == taskId);
    notifyListeners();
    print("Task $taskId deleted successfully!");
  }

  // fetchTasks method for fetching tasks from the TaskService, filtering out
  // deleted tasks, and notifying listeners about the changes.
  Future<void> fetchTasks() async {
    try {
      // Fetching tasks from the TaskService and filtering out deleted tasks.
      final tasksFromApi = await _taskService.fetchAllTasks();
      _tasks = tasksFromApi
          .where((task) => !_taskService.isTaskDeleted(task.id))
          .toList();

      // Reversing the tasks list to display the latest task at the top.
      _tasks = _tasks.reversed.toList();

      notifyListeners();
      print("Tasks fetched successfully!");
    } catch (error, stackTrace) {
      print('Error fetching tasks: $error\n$stackTrace');
    }
  }

  // selectTask method for selecting a task with the given taskId, updating
  // the _selectedTask property, and notifying listeners about the changes.
  void selectTask(String id) {
    final task = _tasks.firstWhereOrNull((t) => t.id == id);

    if (task != null) {
      _selectedTask = task;
      print("Selected task with ID: ${task.id} and Title: ${task.title}");
      notifyListeners(); // Notify listeners to rebuild UI
    } else {
      final errorMessage =
          "Error: Attempted to select a task with ID: $id that does not exist in the data source.";
      print(errorMessage);
      throw ArgumentError(errorMessage);
    }
  }

  // deselectTask method for resetting the _selectedTask property and notifying
  // listeners about the changes.
  void deselectTask() {
    _selectedTask = null;
    print("Deselected the current task.");
    notifyListeners(); // Notify listeners to rebuild UI
  }

  // selectTestSuite method for selecting a test suite and updating the
  // _selectedTestSuite property.
  void selectTestSuite(
