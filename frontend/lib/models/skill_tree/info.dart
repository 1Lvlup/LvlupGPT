// This class, `Info`, represents an object containing information about a certain topic.
class Info {
  // The `difficulty` field is a final variable that stores the level of difficulty
  // associated with the information.
  final String difficulty;

  // The `description` field is a final variable that stores a brief explanation
  // or summary of the information.
  final String description;

  // The `sideEffects` field is a final variable that stores a list of potential
  // side effects or consequences related to the information.
  final List<String> sideEffects;

  // The constructor for the `Info` class takes three required parameters:
  // `difficulty`, `description`, and `sideEffects`. These parameters are used
  // to initialize the corresponding final fields.
  Info({
    required this.difficulty,
    required this.description,
    required this.sideEffects,
  });


