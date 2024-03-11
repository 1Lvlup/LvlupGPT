import 'package:auto_gpt_flutter_client/models/benchmark/api_type.dart';
import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_run.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';

/// A service class responsible for handling interactions with the leaderboard.
/// This class uses the provided [RestApiUtility] instance to make API calls.
class LeaderboardService {
  /// The RestApiUtility instance used to make API calls.
  final RestApiUtility api;

  /// Initializes a new instance of the LeaderboardService class.
  ///
  /// [api] is the RestApiUtility instance used to make API calls.
  LeaderboardService(this.api);

  /// Submits a benchmark report to the leaderboard.
  ///
  /// [benchmarkRun] is a BenchmarkRun object representing the data of a completed benchmark.
  ///
  /// Returns a Future that resolves to a Map<String, dynamic> object representing
  /// the response from the API.
  ///
  /// Throws an Exception if there is an error while submitting the report.
  Future<Map<String, dynamic>> submitReport(BenchmarkRun benchmarkRun) async {
    try {
      // Query the API to submit the benchmark report.
      // Use the provided RestApiUtility instance to make the API call.
      // The API endpoint is 'api/reports'.
      // The request method is PUT.
      // The request body is the JSON representation of the benchmarkRun object.
      // The ApiType is set to ApiType.leaderboard.
      return await api.put(
        'api/reports', // The API endpoint.
        benchmarkRun.toJson(), // The request body.
        apiType: ApiType.leaderboard, // The ApiType.
      );
    } catch (e) {
      // If there is an error while submitting the report, throw an Exception.
      throw Exception('Failed to submit the report to the leaderboard: $e
