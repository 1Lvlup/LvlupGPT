import 'package:auto_gpt_flutter_client/models/step_request_body.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  // Begin a new test group for the StepRequestBody class
  group('StepRequestBody', () {
    // Define a test to check if StepRequestBody creates an instance with correct values
    test('should create StepRequestBody with correct values', () {
      // Create an instance of StepRequestBody with input and additionalInput
      final stepRequestBody = StepRequestBody(
          input: 'Execute something', additionalInput: {'key': 'value'});

      // Assert that the input and additionalInput values are as expected
      expect(stepRequestBody.input, 'Execute something');
      expect(stepRequestBody.additionalInput, {'key': 'value'});
    });

    // Define a test to check if StepRequestBody can be converted to the correct JSON
    test('should convert StepRequestBody to correct JSON', () {
      // Create an instance of StepRequestBody with input and additionalInput
      final stepRequestBody = StepRequestBody(
          input: 'Execute something', additionalInput: {'key': 'value'});

      // Convert the StepRequestBody instance to a JSON map
      final json = stepRequestBody.toJson();

      // Assert that the JSON map has the expected structure
      expect(json, {
        'input': 'Execute something', // The input value
        'additional_input': {'key': 'value'}, // The additionalInput value
      });
    });
  });
}
