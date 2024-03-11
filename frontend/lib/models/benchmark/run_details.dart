/// `RunDetails` encapsulates specific details about a benchmark run.
///
/// This class holds attributes such as the unique run identifier, the command used to initiate the run,
/// the time of completion, the time when the benchmark started, and the name of the test.
class RunDetails {
  /// The unique identifier for the benchmark run, typically a UUID.
  final String runId;

  /// The command used to initiate the benchmark run.
  final String command;

  /// The completion time of the benchmark run as a `DateTime` object.
  final DateTime completionTime;

  /// The start time of the benchmark run as a `DateTime` object.
  final DateTime benchmarkStartTime;

  /// The name of the test associated with this benchmark run.
  final String testName;

  /// Constructs a new `RunDetails` instance.
  ///
  /// [runId]: The unique identifier for the benchmark run.
  /// [command]: The command used to initiate the run.
  /// [completionTime]: The completion time of the run.
  /// [benchmarkStartTime]: The start time of the run.
  /// [testName]: The name of the test.
  RunDetails({
    required this.runId,    /// Assigns the unique identifier for the benchmark run.
    required this.command,  /// Assigns the command used to initiate the run.
    required this.completionTime,  /// Assigns the completion time of the run.
    required this.benchmarkStartTime,  /// Assigns the start time of the run.
    required this.testName,   /// Assigns the name of the test.
  });

  /// Creates a `RunDetails` instance from a map.
  ///
  /// [json]: A map containing key-value pairs corresponding to `RunDetails` fields.
  ///
  /// Returns a new `RunDetails` populated with values from the map.
  factory RunDetails.fromJson(Map<String, dynamic> json) {
    return RunDetails(
      runId: json['run_id'] as String,   /// Retrieves and assigns the run_id from the json map.
      command: json['command'] as String,   /// Retrieves and assigns the command from the json map.
      completionTime: DateTime.parse(json['completion_time'] as String),  /// Retrieves and assigns the completion_time from the json map.
      benchmarkStartTime: DateTime.parse(json['benchmark_start_time'] as String),  /// Retrieves and assigns the benchmark_start_time from the json map.
      testName: json['test_name'] as String,  /// Retrieves and assigns the test_name from the json map.
    );
  }

  /// Converts the `RunDetails` instance to a map.
  ///
  /// Returns a map containing key-value pairs corresponding to `RunDetails` fields.
  Map<String, dynamic> toJson() => {
        'run_id': runId,  /// Adds the run_id to the map.
        'command': command,  /// Adds the command to the map.
        'completion_time': completionTime.toIso8601String(),  /// Adds the completion_time as an ISO 8601 string to the map.
        'benchmark_start_time': benchmarkStartTime.toIso8601String(),  /// Adds the benchmark_start_time as an ISO 8601 string to the map.
        'test_name': testName,  /// Adds the test_name to the map.
      };
}
