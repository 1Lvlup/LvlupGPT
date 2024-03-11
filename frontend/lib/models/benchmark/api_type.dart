/**
 * Defines the available types of APIs that can be handled by the system.
 */
enum ApiType {
  /**
   * Represents the agent API type.
   */
  Agent = 'agent',

  /**
   * Represents the benchmark API type.
   */
  Benchmark = 'benchmark',

  /**
   * Represents the leaderboard API type.
   */
  Leaderboard = 'leaderboard',

  /**
   * Represents an unknown API type.
   */
  Unknown = 'unknown',
}

/**
 * Handles the provided API type by executing the appropriate logic for each type.
 * @param {ApiType} type - The API type to be handled.
 */
function handleApiType(type: ApiType) {
  switch (type) {
    case ApiType.Agent:
      // Handle agent API type
      break;
    case ApiType.Benchmark:
      // Handle benchmark API type
      break;
    case ApiType.Leaderboard:
      // Handle leaderboard API type
      break;
    case ApiType.Unknown:
      // Handle unknown API type
      break;
  }
}
