import 'package:auto_gpt_flutter_client/models/task.dart';

class TestSuite {
  final String timestamp;
  final List<Task> tests;

  TestSuite({required this.timestamp, required this.tests});

  // Serialization: Convert the object into a Map
  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp,
      'tests': tests.map((task) => task.toJson()).toList(),
    };
  }

// Deserialization: Create an object from a Map
  factory TestSuite.fromJson(Map<String, dynamic> json) {
    return TestSuite(
      timestamp: json['timestamp'] as String,
      tests: (json['tests'] as List<dynamic>)
          .map((taskJson) => Task.fromMap(taskJson as Map<String, dynamic>))
          .toList(),
    );
  }
}
