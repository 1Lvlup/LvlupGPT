import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_run.dart';
import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_step_request_body.dart';
import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_task_request_body.dart';
import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_task_status.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_edge.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_node.dart';
import 'package:auto_gpt_flutter_client/models/step.dart';
import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/test_option.dart';
import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/services/benchmark_service.dart';
import 'package:auto_gpt_flutter_client/services/leaderboard_service.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'package:auto_gpt_flutter_client/utils/stack.dart';

class TaskQueueViewModel extends ChangeNotifier {
  // Dependencies are injected via constructor
  final BenchmarkService benchmarkService;
  final LeaderboardService leaderboardService;
  final SharedPreferencesService prefsService;

  // Track if a benchmark is currently running
  bool isBenchmarkRunning = false;

  // Store benchmark statuses for each node in the skill tree
  Map<SkillTreeNode, BenchmarkTaskStatus> benchmarkStatusMap = {};

  // Store the current benchmark runs
  List<BenchmarkRun> currentBenchmarkRuns = [];

  // Selected node hierarchy and selected test option
  List<SkillTreeNode>? _selectedNodeHierarchy;
  TestOption _selectedOption = TestOption.runSingleTest;

  // Getters for selected node hierarchy and selected test option
  TestOption get selectedOption => _selectedOption;
  List<SkillTreeNode>? get selectedNodeHierarchy => _selectedNodeHierarchy;

  // Constructor
  TaskQueueViewModel(
      this.benchmarkService, this.leaderboardService, this.prefsService);

  // Method to update the selected node hierarchy based on the selected test option
  void updateSelectedNodeHierarchyBasedOnOption(
      TestOption selectedOption,
      SkillTreeNode? selectedNode,
      List<SkillTreeNode> nodes,
      List<SkillTreeEdge> edges) {
    _selectedOption = selectedOption;
    switch (selectedOption) {
      case TestOption.runSingleTest:
        _selectedNodeHierarchy = selectedNode != null ? [selectedNode] : [];
        break;

      case TestOption.runTestSuiteIncludingSelectedNodeAndAncestors:
        if (selectedNode != null) {
          populateSelectedNodeHierarchy(selectedNode.id, nodes, edges);
        }
        break;

      case TestOption.runAllTestsInCategory:
        if (selectedNode != null) {
          _getAllNodesInDepthFirstOrderEnsuringParents(nodes, edges);
        }
        break;
    }
    notifyListeners();
  }

  // Method to populate the selected node hierarchy recursively
  void recursivePopulateHierarchy(String nodeId, Set<String> addedNodes,
      List<SkillTreeNode> nodes, List<SkillTreeEdge> edges) {
    // ... (rest of the method)
  }

  // Method to run the benchmark
  Future<void> runBenchmark(
      ChatViewModel chatViewModel, TaskViewModel taskViewModel) async {
    // ... (rest of the method)
  }

  // Method to submit benchmark runs to the leaderboard
  Future<void> submitToLeaderboard(
      String teamName, String repoUrl, String agentGitCommitSha) async {
    // ... (rest of the method)
  }

  // Helper methods for populating the selected node hierarchy
  void populateSelectedNodeHierarchy(String startNodeId,
      List<SkillTreeNode> nodes, List<SkillTreeEdge> edges) {
    _selectedNodeHierarchy = <SkillTreeNode>[];
    final addedNodes = <String>{};
    recursivePopulateHierarchy(startNodeId, addedNodes, nodes, edges);
    notifyListeners();
  }

  List<SkillTreeNode> _getParentsOfNodeUsingEdges(
      String nodeId, List<SkillTreeNode> nodes, List<SkillTreeEdge> edges) {
    // ... (rest of the method)
  }

  List<SkillTreeNode> _getChildrenOfNodeUsingEdges(
      String nodeId, List<SkillTreeNode> nodes, List<SkillTreeEdge> edges) {
    // ... (rest of the method)
  }

  void _getAllNodesInDepthFirstOrderEnsuringParents(
      List<SkillTreeNode> skillTreeNodes, List<SkillTreeEdge> skillTreeEdges) {
    // ... (rest of the method)
  }
}
