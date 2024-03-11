import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/task_request_body.dart';
import 'package:auto_gpt_flutter_client/models/task_response.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';

/// Service class for performing task-related operations.
class TaskService {
  final RestApiUtility _api;
  final SharedPreferencesService _prefsService;
  List<String> _deletedTaskIds = []; // List to store deleted task IDs

  TaskService(this._api, this._prefsService);

  /// Creates a new task.
  ///
  /// [taskRequestBody] is a Map representing the request body for creating a task.
  Future<Map<String, dynamic>> createTask(TaskRequestBody taskRequestBody) async {
    try {
      // Calls the API to create a new task
      return await _api.post('agent/tasks', taskRequestBody.toJson());
    } catch (e) {
      rethrow; // Rethrows the exception to be handled by the caller
    }
  }

  /// Fetches a single page of tasks.
  ///
  /// [currentPage] and [pageSize] are pagination parameters.
  Future<TaskResponse> fetchTasksPage({
    required int currentPage,
    required int pageSize,
  }) async {
    try {
      // Calls the API to fetch a single page of tasks
      final response = await _api.get(
        'agent/tasks?current_page=$currentPage&page_size=$pageSize',
      );
      // Maps the API response to the TaskResponse model
      return TaskResponse.fromJson(response);
    } catch (e) {
      throw Exception('Failed to fetch a page of tasks: $e');
    }
  }

  /// Fetches all tasks across all pages.
  Future<List<Task>> fetchAllTasks({int pageSize = 10000}) async {
    int currentPage = 1;
    List<Task> allTasks = [];

    while (true) {
      // Fetches a single page of tasks and adds them to the allTasks list
      final response = await fetchTasksPage(
        currentPage: currentPage,
        pageSize: pageSize,
      );
      allTasks.addAll(response.tasks);

      if (response.tasks.length < pageSize) {
        break;
      }
      currentPage++;
    }
    return allTasks;
  }

  /// Gets details about a specific task.
  ///
  /// [taskId] is the ID of the task.
  Future<Map<String, dynamic>> getTaskDetails(String taskId) async {
    try {
      // Calls the API to get details about a specific task
      return await _api.get('agent/tasks/$taskId');
    } catch (e) {
      throw Exception('Failed to get task details: $e');
    }
  }

  /// Lists all artifacts for a specific task.
  ///
  /// [taskId] is the ID of the task.
  /// [currentPage] and [pageSize] are optional pagination parameters.
  Future<Map<String, dynamic>> listTaskArtifacts(
    String taskId, {
    int currentPage = 1,
    int pageSize = 10,
  }) async {
    try {
      // Calls the API to list all artifacts for a specific task
      return await _api.get(
        'agent/tasks/$taskId/artifacts?current_page=$currentPage&page_size=$pageSize',
      );
    } catch (e) {
      throw Exception('Failed to list task artifacts: $e');
    }
  }

  /// Loads deleted tasks from the shared preferences.
  Future<void> loadDeletedTasks() async {
    _deletedTaskIds = _prefsService.getStringList('deletedTasks') ?? [];
    print("Deleted tasks fetched successfully!");
  }

  /// Saves a deleted task to the shared preferences.
  ///
  /// [taskId] is the ID of the deleted task.
  void saveDeletedTask(String taskId) {
    _deletedTaskIds.add(taskId);
    _prefsService.setStringList('deletedTasks', _deletedTaskIds);
    print("Task $taskId deleted successfully!");
  }

  /// Checks if a task is deleted.
  ///
  /// [taskId] is the ID of the task to check.
  bool isTaskDeleted(String taskId) {
    return _deletedTaskIds.contains(taskId);
  }
}

