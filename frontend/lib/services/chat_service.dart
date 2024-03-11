import 'dart:io';
import 'dart:typed_data';
import 'package:auto_gpt_flutter_client/models/step_request_body.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';
import 'dart:html' as html;

/// Service class for performing chat-related operations.
class ChatService {
  /// Creates an instance of the ChatService class.
  ///
  /// [api] is the RestApiUtility instance used for API calls.
  ChatService(this.api);

  /// Executes a step in a specific task.
  ///
  /// [taskId] is the ID of the task.
  /// [stepRequestBody] is a Map representing the request body for executing a step.
  ///
  /// Returns a Future that resolves to a Map containing the response data.
  Future<Map<String, dynamic>> executeStep(
      String taskId, StepRequestBody stepRequestBody) async {
    try {
      // Makes a POST request to the API endpoint.
      // Returns the decoded JSON response.
      return await api.post('agent/tasks/$taskId/steps', stepRequestBody.toJson());
    } catch (e) {
      // TODO: We are bubbling up the full response. Revisit this.
      rethrow;
    }
  }

  /// Gets details about a specific task step.
  ///
  /// [taskId] is the ID of the task.
  /// [stepId] is the ID of the step.
  ///
  /// Returns a Future that resolves to a Map containing the response data.
  Future<Map<String, dynamic>> getStepDetails(
      String taskId, String stepId) async {
    try {
      // Makes a GET request to the API endpoint.
      // Returns the decoded JSON response.
      return await api.get('agent/tasks/$taskId/steps/$stepId');
    } catch (e) {
      throw Exception('Failed to get step details: $e');
    }
  }

  /// Lists all steps for a specific task.
  ///
  /// [taskId] is the ID of the task.
  /// [currentPage] and [pageSize] are optional pagination parameters.
  ///
  /// Returns a Future that resolves to a Map containing the response data.
  Future<Map<String, dynamic>> listTaskSteps(String taskId,
      {int currentPage = 1, int pageSize = 10}) async {
    try {
      // Makes a GET request to the API endpoint with pagination parameters.
      // Returns the decoded JSON response.
      return await api.get(
          'agent/tasks/$taskId/steps?current_page=$currentPage&page_size=$pageSize');
    } catch (e) {
      throw Exception('Failed to list task steps: $e');
    }
  }

  /// Uploads an artifact for a specific task.
  ///
  /// [taskId] is the ID of the task.
  /// [artifactFile] is the File to be uploaded.
  /// [uri] is the URI of the artifact.
  ///
  /// Returns a Future that resolves to a Map containing the response data.
  Future<Map<String, dynamic>> uploadArtifact(
      String taskId, File artifactFile, String uri) async {
    // Placeholder implementation.
    return Future.value({'status': 'Not implemented yet'});
  }

  /// Downloads a specific artifact.
  ///
  /// [taskId] is the ID of the task.
  /// [artifactId] is the ID of the artifact.
  ///
  /// Throws an exception if there's an error during the download.
  Future<void> downloadArtifact(String taskId, String artifactId) async {
    try {
      // Makes a GET request to the API endpoint to download the artifact.
      // Converts the response to a Uint8List.
      final Uint8List bytes =
          await api.getBinary('agent/tasks/$taskId/artifacts/$artifactId');

      // Creates a Blob from the Uint8List.
      final blob = html.Blob([bytes]);

      // Generates a URL from the Blob.
      final url = html.Url.createObjectUrlFromBlob(blob);

      // Creates an anchor HTML element with the URL and downloads the artifact.
      final anchor = html.AnchorElement(href: url)
        ..setAttribute("download", "artifact_$artifactId")
        ..click();

      // Cleanup: Revokes the object URL.
      html.Url.revokeObjectUrl(url);
    } catch (e) {
      throw Exception('An error occurred while downloading the artifact: $e');
   
