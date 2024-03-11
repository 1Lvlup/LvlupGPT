import 'dart:convert';
import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/services/task_service.dart';
import 'package:flutter/foundation.dart';
import 'package:collection/collection.dart';

class TaskViewModel with ChangeNotifier {
  final TaskService _taskService;
  final SharedPreferencesService _prefsService;

  List<Task> _tasks = [];
  List<TestSuite> _testSuites = [];
  List<Task> _tasksDataSource = [];
  List<TestSuite> _testSuitesDataSource = [];

  Task? _selectedTask;
  TestSuite? _selectedTestSuite;

  bool _isWaitingForAgentResponse = false;

  bool get isWaitingForAgentResponse => _isWaitingForAgentResponse;

  TaskViewModel(this._taskService, this._prefsService);

  /// Returns the currently selected task.
  Task? get selectedTask => _selectedTask;
  TestSuite? get selectedTestSuite => _selectedTestSuite;

  /// Adds a task and returns its ID.
  Future<String> createTask(String title) async {
    _isWaitingForAgentResponse = true;
    notifyListeners();
    try {
      final newTask = TaskRequestBody(input: title);
      // Add to data source
      final createdTask = await _taskService.createTask(newTask);
      // Create a Task object from the created task response
      final newTaskObject =
          Task(id: createdTask['task_id'], title: createdTask['input']);

      _tasks.add(newTaskObject);
      _tasksDataSource.add(newTaskObject);

      _tasks = _tasks.reversed.toList();

      notifyListeners();

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

  /// Deletes a task.
  void deleteTask(String taskId) {
    _taskService.saveDeletedTask(taskId);
    _tasks.removeWhere((task) => task.id == taskId);
    _tasksDataSource.removeWhere((task) => task.id == taskId);
    notifyListeners();
    print("Task $taskId deleted successfully!");
  }

  /// Fetches tasks from the data source.
  Future<void> fetchTasks() async {
    try {
      final tasksFromApi = await _taskService.fetchAllTasks();
      _tasks = tasksFromApi
          .where((task) => !_taskService.isTaskDeleted(task.id))
          .toList();

      _tasks = _tasks.reversed.toList();

      notifyListeners();
      print("Tasks fetched successfully!");
    } catch (error, stackTrace) {
      print('Error fetching tasks: $error\n$stackTrace');
    }
  }

  /// Handles the selection of a task by its ID.
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

  /// Deselects the currently selected task.
  void deselectTask() {
    _selectedTask = null;
    print("Deselected the current task.");
    notifyListeners(); // Notify listeners to rebuild UI
  }

  void selectTestSuite(TestSuite testSuite) {
    _selectedTestSuite = testSuite;
    notifyListeners();
  }

  void deselectTestSuite() {
    _selectedTestSuite = null;
    notifyListeners();
  }

  // Helper method to save test suites to SharedPreferences
  Future<void> _saveTestSuitesToPrefs() async {
    final testSuitesToStore =
        _testSuites.map((testSuite) => jsonEncode(testSuite.toJson())).toList();
    await _prefsService.setStringList('testSuites', testSuitesToStore);
  }

  // Adds a new test suite and saves it to SharedPreferences
  void addTestSuite(TestSuite testSuite) async {
    _testSuites.add(testSuite);
    await _saveTestSuitesToPrefs();
    notifyListeners();
    print("Test suite successfully added!");
  }

  // Fetch test suites from SharedPreferences
  Future<void> fetchTestSuites() async {
    final storedTestSuites =
        await _prefsService.getStringList('testSuites') ?? [];
    _testSuites = storedTestSuites
        .map((testSuiteMap) => TestSuite.fromJson(jsonDecode(testSuiteMap)))
        .toList();
    notifyListeners();
  }

  // The fetchAndCombineData method performs several tasks:
  // 1. It fetches the tasks and filters out deleted ones.
  // 2. It fetches the test suites from SharedPreferences.
  // 3. It combines both the tasks and test suites into a single data source according to specified logic.
  Future<void> fetchAndCombineData() async {
    // Step 1: F
