enum ApiType {
  Agent = 'agent',
  Benchmark = 'benchmark',
  Leaderboard = 'leaderboard',
  Unknown = 'unknown',
}

// Usage example:
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
