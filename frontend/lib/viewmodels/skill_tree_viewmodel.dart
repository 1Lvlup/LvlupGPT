import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:graphview/GraphView.dart';

// Import custom models for the skill tree
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_category.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_edge.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_node.dart';

/// A ViewModel for managing the SkillTree data and UI state
class SkillTreeViewModel extends ChangeNotifier {
  // Private list of SkillTreeNodes
  List<SkillTreeNode> _skillTreeNodes = [];

  /// List of SkillTreeNodes
  List<SkillTreeNode> get skillTreeNodes => _skillTreeNodes;

  // Private list of SkillTreeEdges
  List<SkillTreeEdge> _skillTreeEdges = [];

  /// List of SkillTreeEdges
  List<SkillTreeEdge> get skillTreeEdges => _skillTreeEdges;

  // Selected SkillTreeNode
  SkillTreeNode? _selectedNode;

  /// Selected SkillTreeNode
  SkillTreeNode? get selectedNode => _selectedNode;

  /// Graph object for visualizing the skill tree
  final Graph graph = Graph();

  /// Configuration for the Sugiyama layout algorithm
  SugiyamaConfiguration builder = SugiyamaConfiguration();

  /// Current SkillTreeCategory
  SkillTreeCategory currentSkillTreeType = SkillTreeCategory.general;

  /// Initialize the SkillTree by reading JSON data from assets
  Future<void> initializeSkillTree() async {
    try {
      resetState();

      // Determine the JSON file name based on the current skill tree type
      String fileName = currentSkillTreeType.jsonFileName;

      // Read the JSON file from assets
      String jsonContent = await rootBundle.loadString('assets/$fileName');

      // Decode the JSON string
      Map<String, dynamic> decodedJson = jsonDecode(jsonContent);

      // Create SkillTreeNodes from the decoded JSON
      for (var nodeMap in decodedJson['nodes']) {
        SkillTreeNode node = SkillTreeNode.fromJson(nodeMap);
        _skillTreeNodes.add(node);
      }

      // Create SkillTreeEdges from the decoded JSON
      for (var edgeMap in decodedJson['edges']) {
        SkillTreeEdge edge = SkillTreeEdge.fromJson(edgeMap);
        _skillTreeEdges.add(edge);
      }

      // Configure the Sugiyama layout algorithm
      builder.orientation = (SugiyamaConfiguration.ORIENTATION_LEFT_RIGHT);
      builder.bendPointShape = CurvedBendPointShape(curveLength: 20);

      notifyListeners();

      return Future.value(); // Explicitly return a completed Future
    } catch (e) {
      print(e);
    }
  }

  /// Reset the SkillTree state
  void resetState() {
    _skillTreeNodes = [];
    _skillTreeEdges = [];
    _selectedNode = null;
  }

  /// Toggle the selection of a SkillTreeNode
  void toggleNodeSelection(String nodeId) {
    if (_selectedNode?.id == nodeId) {
      // Unselect the node if it's already selected
      _selectedNode = null;
    } else {
      // Select the new node
      _selectedNode = _skillTreeNodes.firstWhere((node) => node.id == nodeId);
    }
    notifyListeners();
  }

  /// Get a SkillTreeNode by its ID
  SkillTreeNode? getNodeById(String nodeId) {
    try {
      // Find the node in the list where the ID matches
      return _skillTreeNodes.firstWhere((node) => node.id == nodeId);
    } catch (e) {
      print("Node with ID $nodeId not found: $e");
      return null;
    }
  }
}

