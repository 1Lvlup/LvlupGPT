import 'package:auto_gpt_flutter_client/models/step.dart';
import 'package:auto_gpt_flutter_client/models/step_request_body.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:flutter/foundation.dart';
import 'package:auto_gpt_flutter_client/services/chat_service.dart';
import 'package:auto_gpt_flutter_client/models/chat.dart';
import 'package:auto_gpt_flutter_client/models/message_type.dart';

class ChatViewModel with ChangeNotifier {
  // The ChatService instance used for interacting with the chat API.
  final ChatService _chatService;

  // The list of chats for the current task.
  List<Chat> _chats;

  // The ID of the current task.
  String? _currentTaskId;

  // The instance of SharedPreferencesService for managing shared preferences.
  final SharedPreferencesService _prefsService;

  // A flag indicating whether the view model is waiting for an agent response.
  bool _isWaitingForAgentResponse;

  // A flag indicating whether the continuous mode is enabled.
  bool _isContinuousMode;

  // Constructor for ChatViewModel with required dependencies.
  ChatViewModel(this._chatService, this._prefsService) {
    _chats = [];
    _isWaitingForAgentResponse = false;
    _isContinuousMode = false;
  }

  // Getter for isWaitingForAgentResponse.
  bool get isWaitingForAgentResponse => _isWaitingForAgentResponse;

  // Getter for isContinuousMode.
  bool get isContinuousMode => _isContinuousMode;

  // Getter for prefsService.
  SharedPreferencesService get prefsService => _prefsService;

  // Getter for chats.
  List<Chat> get chats => _chats;

  // Getter for currentTaskId.
  String? get currentTaskId => _currentTaskId;

  // Setter for currentTaskId.
  void setCurrentTaskId(String taskId) {
    if (_currentTaskId != taskId) {
      _currentTaskId = taskId;
      _chats.clear();
      _isWaitingForAgentResponse = false;
      notifyListeners();
      fetchChatsForTask();
    }
  }

  // Clear the current task and chats.
  void clearCurrentTaskAndChats() {
    _currentTaskId = null;
    _chats.clear();
    notifyListeners();
  }

  // Fetch chats for the current task.
  void fetchChatsForTask() async {
    if (_currentTaskId == null) {
      print("Error: Task ID is not set.");
      return;
    }
    try {
      final stepsResponse =
          await _chatService.listTaskSteps(_currentTaskId!, pageSize: 10000);

      // Process the steps and create Chat instances.
      final stepsJsonList = stepsResponse['steps'] ?? [];

      List<Step> steps =
          stepsJsonList.map((stepMap) => Step.fromMap(stepMap)).toList();

      List<Chat> chats = [];

      DateTime currentTimestamp = DateTime.now();

      for (int i = 0; i < steps.length; i++) {
        Step step = steps[i];

        if (step.input.isNotEmpty) {
          // Add user chat.
          chats.add(Chat(
              id: step.stepId,
              taskId: step.taskId,
              message: step.input,
              timestamp: currentTimestamp,
              messageType: MessageType.user,
              artifacts: step.artifacts));
        }

        // Add agent chat.
        chats.add(Chat(
            id: step.stepId,
            taskId: step.taskId,
            message: step.output,
            timestamp: currentTimestamp,
            messageType: MessageType.agent,
            jsonResponse: stepsJsonList[i],
            artifacts: step.artifacts));
      }

      if (chats.isNotEmpty) {
        _chats = chats;
      }

      notifyListeners();

      print(
          "Chats (and steps) fetched successfully for task ID: $_currentTaskId");
    } catch (error) {
      print("Error fetching chats: $error");
      // TODO: Handle additional error scenarios or log them as required
    }
  }

  // Send a chat message and handle the response.
  void sendChatMessage(String? message,
      {required int continuousModeSteps, int currentStep = 1}) async {
    if (_currentTaskId == null) {
      print("Error: Task ID is not set.");
      return;
    }
    _isWaitingForAgentResponse = true;
    notifyListeners();

    try {
      StepRequestBody requestBody = StepRequestBody(input: message);

      Map<String, dynamic> executedStepResponse =
          await _chatService.executeStep(_currentTaskId!, requestBody);

      Step executedStep = Step.fromMap(executedStepResponse);

      if (executedStep.input.isNotEmpty) {
        // Add user chat.
        final userChat = Chat(
            id: executedStep.stepId,
            taskId: executedStep.taskId,
            message: executedStep.input,
            timestamp: DateTime.now(),
            messageType: MessageType.user,
            artifacts: executedStep.artifacts);

        _chats.add(userChat);
      }

      // Add agent chat.
      final agentChat = Chat(
          id: executedStep.stepId,
          taskId: executedStep.taskId,
          message: executedStep.output,
          timestamp: DateTime.now(),
          messageType: MessageType.agent,
          jsonResponse: executedStepResponse,
          artifacts: executedStep.artifacts);

      _chats.add(agentChat);

