class StepRequestBody {
  final String? input;
  final Map<String, dynamic>? additionalInput;

  StepRequestBody({required this.input, this.additionalInput});

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

  /// Returns `true` if both `input` and `additionalInput` are `null`.
  bool get isEmpty => input == null && additionalInput == null;
}

