import 'package:auto_gpt_flutter_client/models/task.dart';

/// A class representing a TestSuite which contains a list of tasks and a timestamp.
class TestSuite {
  /// The timestamp of the test suite.
  final String timestamp;

  /// The list of tasks in the test suite.
  final List<Task> tests;

  /// Constructor for the TestSuite class.
  ///
  /// Parameters:
  /// - timestamp: The timestamp of the test suite.
  /// - tests: The list of tasks in the test suite.
  TestSuite({required this.timestamp, required this.tests});

  /// Serialization method for the TestSuite class.
  ///
  /// This method converts the TestSuite object into a Map<String, dynamic> format.
  /// It is useful for sending data over the network or storing it in a database.
  ///
  /// Returns:
  /// A Map<String, dynamic> representation of the TestSuite object.
  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp, // The timestamp of the test suite.
      'tests': tests.map((task) => task.toJson()).toList(), // The list of tasks in the test suite.
    };
  }

  /// Deserialization method for the TestSuite class.
  ///
  /// This method creates a TestSuite object from a Map<String, dynamic> format.
  /// It is useful for receiving data over the network or retrieving it from a database.
  ///
  /// Parameters:
  /// - json: A Map<String, dynamic> representation of the TestSuite object.
  ///
  /// Returns:
  /// A TestSuite object created from the given Map<String, dynamic> representation.
  factory TestSuite.fromJson(Map<String, dynamic> json) {
    return TestSuite(
      timestamp: json['timestamp'] as String, // The timestamp of the test suite.
      tests: (json['tests'] as List<dynamic>) // The list of tasks in the test suite.
          .map((taskJson) => Task.fromMap(taskJson as Map<String
