/// The `TaskRequestBody` class represents the request body for a task.
class TaskRequestBody {
  /// The `input` variable holds the required input for the task.
  final String input;

  /// The `additionalInput` variable is an optional map that can hold any
  /// additional input data for the task.
  final Map<String, dynamic>? additionalInput;

  /// The constructor for the `TaskRequestBody` class. Takes in a required
  /// `input` string and an optional `additionalInput` map.
  TaskRequestBody({required this.input, this.additionalInput});

  /// The `toJson` method converts the `TaskRequestBody` object into a JSON
  /// map that can be sent as a request body.
  Map<String, dynamic> toJson() {
    return {'input': input, 'additional_input': additionalInput};
  }
}
