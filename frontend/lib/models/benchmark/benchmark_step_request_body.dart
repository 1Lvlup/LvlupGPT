class BenchmarkStepRequestBody {
  final String? input;

  BenchmarkStepRequestBody({required this.input});

  Map<String, dynamic> toJson() {
    final jsonMap = <String, dynamic>{};
    if (input != null) {
      jsonMap['input'] = input;
    }
    return jsonMap;
  }

  /// Constructs an instance of BenchmarkStepRequestBody from a JSON map.
  factory BenchmarkStepRequestBody.fromJson(Map<String, dynamic> json) {
    return BenchmarkStepRequestBody(
      input: json['input'] as String?,
    );
  }
}

