/// Represents a task or topic the user wants to discuss with the agent.
class Task {
  /// The unique identifier of the task.
  final String id;

  /// Additional input provided by the user for the task.
  /// This is an optional field and can be null.
  final Map<String, dynamic>? additionalInput;

  /// Artifacts related to the task.
  /// This is an optional field and can be null.
  final List<String>? artifacts;

  /// The title of the task.
  /// This field is nullable and can be set or retrieved using the [title] getter/setter.
  String? _title;

  /// Constructor for the [Task] class.
  ///
  /// The [id] field is required, while [additionalInput] and [artifacts] are optional.
  /// The [title] field is also optional and can be set later using the [title] setter.
  Task({
    required this.id,
    this.additionalInput,
    this.artifacts,
  }) : _title = null;

  /// Getter for the [title] field.
  String? get title => _title;

  /// Setter for the [title] field.
  ///
  /// Throws an [ArgumentError] if the new title is empty.
  set title(String? newTitle) {
    if (newTitle?.isNotEmpty ?? false) {
      _title = newTitle;
    } else {
      throw ArgumentError('Title cannot be empty.');
    }
  }

  /// Converts a Map (usually from JSON) to a Task object.
  ///
  /// The Map should contain the following keys:
  /// - `task_id`: The unique identifier of the task.
  /// - `input`: The title of the task.
  /// - `additional_input`: Additional input provided by the user for the task.
  ///   This is an optional field and can be null.
  /// - `artifacts`: Artifacts related to the task.
  ///   This is an optional field and can be null.
  factory Task.fromMap(Map<String, dynamic> map) {
    Map<String, dynamic>? additionalInput;
    List<String>? artifacts;

    if (map['additional_input'] != null) {
      additionalInput = Map<String, dynamic>.from(map['additional_input']);
    }

    if (map['artifacts'] != null) {
      artifacts = List<String>.from(map['artifacts'].cast<String>());
    }

    final Task task = Task(
      id: map['task_id'],
      additionalInput: additionalInput
