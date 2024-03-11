class SkillTreeEdge {
  // The unique identifier for this skill tree edge.
  final String id;

  // The identifier of the node that this edge originates from.
  final String from;

  // The identifier of the node that this edge points to.
  final String to;

  // The type of arrow that should be displayed for this edge.
  final String arrows;

  SkillTreeEdge({
    // Required: The unique identifier for this skill tree edge.
    required this.id,

    // Required: The identifier of the node that this edge originates from.
    required this.from,

    // Required: The identifier of the node that this edge points to.
    required this.to,

    // Required: The type of arrow that should be displayed for this edge.
    required this.arrows,
  });

  // Optionally, add a factory constructor to initialize a SkillTreeEdge
  // object from a JSON object.
  factory SkillTreeEdge.fromJson(Map<String, dynamic> json) {
    // Initialize a new SkillTreeEdge object with the given JSON data.
    return SkillTreeEdge(
      id: json['id'], // The unique identifier for this skill tree edge.
      from: json['from'], // The identifier of the node that this edge originates from.
      to: json['to'], // The identifier of the node that this edge points to.
      arrows: json['arrows'], // The type of arrow that should be displayed for this edge.
    );
  }
}
