class StepRequestBody {
  // The `input` variable holds the primary input data of type String.
  final String? input;

  // The `additionalInput` variable is an optional map that can store
  // additional input data of type Map<String, dynamic>.
  final Map<String, dynamic>? additionalInput;

  // The constructor `StepRequestBody` takes two parameters: `input` and
  // `additionalInput`. The `input` parameter is required, while
  // `additionalInput` is optional.
  StepRequestBody({required this.input, this.additionalInput});

  // The `toJson` method converts the instance variables into a JSON-serializable
  // Map<String, dynamic> object. If `input` is not null, it adds the key-value
  // pair 'input': input to the map. If `additionalInput` is not null, it adds
  // the key-value pair 'additional_input': additionalInput to the map.
  Map<String, dynamic> toJson() {
    final data = <String, dynamic>{};
    if (input != null) {
      data['input'] = input;
    }
    if (additionalInput != null) {
      data['additional_input'] = additionalInput;
    }
    return data;
  }

  // The `isEmpty` getter checks if both `input` and `additionalInput` are null.
  // If both are null, it returns true; otherwise, it returns false.
  bool get isEmpty => input == null && additionalInput == null;
}

