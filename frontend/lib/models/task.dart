/// Represents a task or topic the user wants to discuss with the agent.
class Task {
  final String id;
  final Map<String, dynamic>? additionalInput;
  final List<String>? artifacts;
  String? _title;

  String? get title => _title;

  set title(String? newTitle) {
    if (newTitle?.isNotEmpty ?? false) {
      _title = newTitle;
    } else {
      throw ArgumentError('Title cannot be empty.');
    }
  }

  /// Converts a Map (usually from JSON) to a Task object
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
      additionalInput: additionalInput,
      artifacts: artifacts,
    );

    task._title = map['input'];

    return task;
  }

  Map<String, dynamic> toJson() {
    return {
      'task_id': id,
      'input': _title,
      'additional_input': additionalInput,
      'artifacts': artifacts,
    };
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Task &&
          runtimeType == other.runtimeType &&
          id == other.id &&
          _title == other._title &&
          mapEquals(additionalInput, other.additionalInput) &&
          listEquals(artifacts, other.artifacts);

  @override
  int get hashCode =>
      id.hashCode ^ _title.hashCode ^ hashObjects(additionalInput)
