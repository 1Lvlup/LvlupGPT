import 'dart:convert';
import 'dart:typed_data';
import 'package:auto_gpt_flutter_client/models/benchmark/api_type.dart';
import 'package:http/http.dart' as http;

/// A class responsible for handling REST API requests.
///
/// This class encapsulates the logic for making HTTP requests to different
/// API endpoints based on the provided [ApiType]. It provides methods for GET,
/// POST, PUT, and binary data retrieval.
class RestApiUtility {
  /// The base URL for the agent API.
  String _agentBaseUrl;

  /// The base URL for the benchmark API.
  final String _benchmarkBaseUrl = "http://127.0.0.1:8080/ap/v1";

  /// The base URL for the leaderboard API.
  final String _leaderboardBaseUrl = "https://leaderboard.agpt.co";

  /// Initializes a new instance of the [RestApiUtility] class.
  ///
  /// The [_agentBaseUrl] is initialized with the provided value.
  RestApiUtility(this._agentBaseUrl);

  /// Updates the base URL for the agent API.
  ///
  /// [newBaseURL] - The new base URL for the agent API.
  void updateBaseURL(String newBaseURL) {
    _agentBaseUrl = newBaseURL;
  }

  /// Returns the effective base URL based on the provided [apiType].
  ///
  /// [apiType] - The type of API to get the base URL for.
  String _getEffectiveBaseUrl(ApiType apiType) {
    switch (apiType) {
      case ApiType.agent:
        return _agentBaseUrl;
      case ApiType.benchmark:
        return _benchmarkBaseUrl;
      case ApiType.leaderboard:
        return _leaderboardBaseUrl;
      default:
        return _agentBaseUrl;
    }
  }

  /// Sends a GET request to the specified [endpoint] for the given [apiType].
  ///
  /// [endpoint] - The endpoint to send the request to.
  /// [apiType] - The type of API to send the request to.
  ///
  /// Returns a [Future] that resolves to a [Map] containing the decoded JSON
  /// response body.
  Future<Map<String, dynamic>> get(String endpoint,
      {ApiType apiType = ApiType.agent}) async {
    final effectiveBaseUrl = _getEffectiveBaseUrl(apiType);
    final response = await _processResponse(await http.get(Uri.parse('$effectiveBaseUrl/$endpoint')), endpoint);
    return response;
  }

  /// Sends a POST request to the specified [endpoint] for the given [apiType]
  /// with the provided [payload].
  ///
  /// [endpoint] - The endpoint to send the request to.
  /// [payload] - The data to send in the request body.
  /// [apiType] - The type of API to send the request to.
  ///
  /// Returns a [Future] that resolves to a [Map] containing the decoded JSON
  /// response body.
  Future<Map<String, dynamic>> post(
      String endpoint, Map<String, dynamic> payload,
      {ApiType apiType = ApiType.agent}) async {
    final effectiveBaseUrl = _getEffectiveBaseUrl(apiType);
    final response = await _processResponse(await http.post(
      Uri.parse('$effectiveBaseUrl/$endpoint'),
      body: json.encode(payload),
      headers: {"Content-Type": "application/json"},
    ), endpoint);
    return response;
  }

  /// Sends a PUT request to the specified [endpoint] for the given [apiType]
  /// with the provided [payload].
  ///
  /// [endpoint] - The endpoint to send the request to.
  /// [payload] - The data to send in the request body.
  /// [apiType] - The type of API to send the request to.
  ///
  /// Returns a [Future] that resolves to a [Map] containing the decoded JSON
  /// response body.
  Future<Map<String, dynamic>> put(
      String endpoint, Map<String, dynamic> payload,
      {ApiType apiType = ApiType.agent}) async {
    final effectiveBaseUrl = _getEffectiveBaseUrl(apiType);
    final response = await _processResponse(await http.put(
      Uri.parse('$effectiveBaseUrl/$
