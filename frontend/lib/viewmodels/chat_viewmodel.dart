import 'package:auto_gpt_flutter_client/models/step.dart';
import 'package:auto_gpt_flutter_client/models/step_request_body.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:flutter/foundation.dart';
import 'package:auto_gpt_flutter_client/services/chat_service.dart';
import 'package:auto_gpt_flutter_client/models/chat.dart';
import 'package:auto_gpt_flutter_client/models/message_type.dart';

class ChatViewModel with ChangeNotifier {
  final ChatService _chatService;
  List<Chat> _chats = [];
  String? _currentTaskId;
  final SharedPreferencesService _prefsService;

  bool _isWaitingForAgentResponse = false;
  bool _isContinuousMode = false;

  bool get isWaitingForAgentResponse => _isWaitingForAgentResponse;
  bool get isContinuousMode => _isContinuousMode;

  SharedPreferencesService get prefsService => _prefsService;

  ChatViewModel(this._chatService, this._prefsService);

  List<Chat> get chats => _chats;

  String? get currentTaskId => _currentTaskId;

  void setCurrentTaskId(String taskId) {
    if (_currentTaskId != taskId) {
      _currentTaskId = taskId;
      _chats.clear();
      _isWaitingForAgentResponse = false;
      notifyListeners();
      fetchChatsForTask();
    }
  }

  void clearCurrentTaskAndChats() {
    _currentTaskId = null;
    _chats.clear();
    notifyListeners();
  }

  void fetchChatsForTask() async {
    if (_currentTaskId == null) {
      print("Error: Task ID is not set.");
      return;
    }
    try {
      final stepsResponse =
          await _chatService.listTaskSteps(_currentTaskId!, pageSize: 10000);

      final stepsJsonList = stepsResponse['steps'] ?? [];

      List<Step> steps =
          stepsJsonList.map((stepMap) => Step.fromMap(stepMap)).toList();

      List<Chat> chats = [];

      DateTime currentTimestamp = DateTime.now();

      for (int i = 0; i < steps.length; i++) {
        Step step = steps[i];

        if (step.input.isNotEmpty) {
          chats.add(Chat(
              id: step.stepId,
              taskId: step.taskId,
              message: step.input,
              timestamp: currentTimestamp,
              messageType: MessageType.user,
              artifacts: step.artifacts));
        }

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
        final userChat = Chat(
            id: executedStep.stepId,
            taskId: executedStep.taskId,
            message: executedStep.input,
            timestamp: DateTime.now(),
            messageType: MessageType.user,
            artifacts: executedStep.artifacts);

        _chats.add(userChat);
      }

      final agentChat = Chat(
          id: executedStep.stepId,
          taskId: executedStep.taskId,
          message: executedStep.output,
          timestamp: DateTime.now(),
          messageType: MessageType.agent,
          jsonResponse: executedStepResponse,
          artifacts: executedStep.artifacts);

      _chats.add(agentChat);

      removeTemporaryMessage();

      notifyListeners();

      if (_isContinuousMode && !executedStep.isLast) {
        if (currentStep < continuousModeSteps) {
          sendChatMessage(null,
              continuousModeSteps: continuousModeSteps,
              currentStep: currentStep + 1);
        } else {
          _isContinuousMode = false;
        }
      }

      print("Chats added for task ID: $_currentTaskId");
    } catch (e) {
      removeTemporaryMessage();
      rethrow;
      // TODO: Handle additional error scenarios or log them as required
    } finally {
      _isWaitingForAgentResponse = false;
      notifyListeners();
    }
  }

  void addTemporaryMessage(String message) {
    Chat tempMessage = Chat(
        id: "TEMP_ID",
        taskId: "TEMP_ID",
        message: message,
        timestamp: DateTime.now(),
        messageType: MessageType.user,
        artifacts: []);

    _chats.add(tempMessage);
    notifyListeners();
  }

