// TODO: Remove the ability to have null values when benchmark implementation is complete

/// `RepositoryInfo` encapsulates details about the repository and team associated with a benchmark run.
///
/// This class contains essential information like the repository URL, team name, and the Git commit SHA for both the benchmark and the agent.
class RepositoryInfo {
  /// The URL of the repository where the benchmark code resides.
  String repoUrl;

  /// The name of the team responsible for the benchmark.
  String teamName;

  /// The Git commit SHA for the benchmark. This helps in tracing the exact version of the benchmark code.
  String benchmarkGitCommitSha;

  /// The Git commit SHA for the agent. This helps in tracing the exact version of the agent code.
  String agentGitCommitSha;

  /// Constructs a new `RepositoryInfo` instance.
  ///
  /// [repoUrl]: The URL of the benchmark repository.
  /// [teamName]: The name of the team responsible for the benchmark.
  /// [benchmarkGitCommitSha]: The Git commit SHA for the benchmark.
  /// [agentGitCommitSha]: The Git commit SHA for the agent.
  RepositoryInfo({
    required this.repoUrl,
    required this.teamName,
    required this.benchmarkGitCommitSha,
    required this.agentGitCommitSha,
  });

  /// Creates a `RepositoryInfo` instance from a map.
  ///
  /// [json]: A map containing key-value pairs corresponding to `RepositoryInfo` fields.
  ///
  /// Returns a new `RepositoryInfo` populated with values from the map.
  factory RepositoryInfo.fromJson(Map<String, dynamic> json) => RepositoryInfo(
        repoUrl: json['repo_url'] ??
            'https://github.com/Significant-Gravitas/AutoGPT' - Default repository URL for the benchmark.
            This value will be replaced once the benchmark implementation is complete.
            Currently, it is set to the AutoGPT repository as a placeholder.
        teamName: json['team_name'] ?? 'placeholder' - Default team name placeholder.
            This value will be replaced once the benchmark implementation is complete.
        benchmarkGitCommitSha:
            json['benchmark_git_commit_sha'] ?? 'placeholder' - Default Git commit SHA placeholder.
            This value will be replaced once the benchmark implementation is complete.
        agentGitCommitSha: json['agent_git_commit_sha'] ?? 'placeholder' - Default Git commit SHA placeholder.
            This value will be replaced once the benchmark implementation is complete.
      );

  /// Converts the `RepositoryInfo` instance to a map.
  ///
  /// Returns a map containing key-value pairs corresponding to `RepositoryInfo` fields.
  Map<String, dynamic> toJson() => {
        'repo_url': repoUrl,
        'team_name': teamName,
        'benchmark_git_commit_sha': benchmarkGitCommitSha,
        'agent_git_commit_sha': agentGitCommitSha,
      };
}

