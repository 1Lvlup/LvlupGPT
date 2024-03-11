import 'package:auto_gpt_flutter_client/models/artifact.dart';
import 'package:auto_gpt_flutter_client/models/message_type.dart';

/// Represents a chat message related to a specific task.
class Chat {
  /// The unique identifier of the chat message.
  final String id;

  /// The identifier of the task associated with the chat message.
  final String taskId;

  /// The content of the chat message.
  final String message;

  /// The timestamp of when the chat message was created.
  final DateTime timestamp;

  /// The type of the chat message.
  final MessageType messageType;

  /// Additional JSON response related to the chat message, if any.
  final Map<String, dynamic>? jsonResponse;

  /// The list of artifacts associated with the chat message.
  final List<Artifact> artifacts;

  Chat({
    required this.id,
    required this.taskId,
    required this.message,
    required this.timestamp,
    required this.messageType,
    this.jsonResponse,
    required this.artifacts,
  });

  /// Creates a new Chat object from a JSON map.
  factory Chat.fromMap(Map<String, dynamic> map) {
    return Chat(
      id: map['id'],
      taskId: map['taskId'],
      message: map['message'],
      timestamp: DateTime.parse(map['timestamp']),
      messageType: MessageType.values.firstWhere(
          (e) => e.toString() == 'MessageType.${map['messageType']}'),
      artifacts: (map['artifacts'] as List)
          .map(
              (artifact) => Artifact.fromJson(artifact as Map<String, dynamic>))
          .toList(),
    );
  }

  /// Checks if this Chat object is equal to another object.
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Chat &&
          runtimeType == other.runtimeType &&
          id == other.id &&
          taskId == other.taskId &&
          message == other.message &&
          timestamp == other.timestamp &&
          messageType == other.messageType &&
          artifacts == other.artifacts;

  /// Calculates the hash code for this Chat object.
  @override
  int get hashCode =>
      id.hashCode ^
      taskId.hashCode ^
      message.hashCode ^
      timestamp.hashCode ^
      messageType.hashCode ^
      artifacts.hashCode;

  /// Returns a string representation of this Chat object.
  @override
  String toString() =>
      'Chat(id: $id, taskId: $taskId, message: $message, timestamp: $timestamp, messageType: $messageType, artifacts: $artifacts)'; // Added artifacts in toString method
}

