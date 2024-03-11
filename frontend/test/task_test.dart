import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  // The main function is the entry point for a Dart test suite.
  // It contains a group of tests for the Task class.

  group('Task', () {
    // The group function allows you to group related tests together.
    // In this case, all tests are related to the Task class.

    // Test the properties of the Task class
    test('Task properties', () {
      // This test checks the properties of the Task class.

      final task = Task(id: 1, title: 'Test Task');

      // expect is a function that checks whether the actual value matches the expected value.
      expect(task.id, 1); // Check if the id is equal to 1
      expect(task.title, 'Test Task'); // Check if the title is equal to 'Test Task'
      expect(task.toString(), 'Task(id: 1, title: Test Task)'); // Check if the string representation is correct
    });

    // Test Task.fromMap method
    test('Task.fromMap', () {
      // This test checks the Task.fromMap method.

      final task = Task.fromMap({'id': 1, 'title': 'Test Task'});

      expect(task.id, 1); // Check if the id is equal to 1
      expect(task.title, 'Test Task'); // Check if the title is equal to 'Test Task'
      expect(task.toString(), 'Task(id: 1, title: Test Task)'); // Check if the string representation is correct
    });

    // Test creating a Task with an empty title
    test('Task with empty title', () {
      // This test checks whether creating a Task with an empty title throws an error.

      expect(
        // expect throws an AssertionError if the callback function throws an exception.
        () => Task(id: 2, title: ''),
        throwsA(isA<AssertionError>()),
        // throwsA checks if the callback function throws an exception of the given type.
        // isA checks if an object is an instance of a given type.
      );
    });

    // Test that two Task objects with the same id and title are equal
    test('Two tasks with same properties are equal', () {
      // This test checks whether two Task objects with the same id and title are equal.

      final task1 = Task(id: 4, title: 'Same Task');
      final task2 = Task(id: 4, title: 'Same Task');

      expect(task1, task2); // Check if task1 is equal to task2
      expect(task1.hashCode == task2.hashCode, isTrue); // Check if the hash codes of task1 and task2 are equal
    });

    // Test that toString() returns a string representation of the Task
    test('toString returns string representation', () {
      // This test checks whether the toString() method returns a string representation of the Task.

      final task = Task(id: 5, title: 'Test toString');

      expect(task.toString(), 'Task(id: 5, title: Test toString)'); // Check if the string representation is correct
    });

    // Test that title of Task can be modified

