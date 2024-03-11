import 'package:http/http.dart' as http;
import 'dart:convert';

class UriUtility {
  static bool isValidUrl(String url) {
    if (url.isEmpty || RegExp(r'[\s<>]').hasMatch(url)) {
      print('URL is either empty or contains spaces/invalid characters.');
      return false;
    }

    if (url.startsWith('mailto:')) {
      print('URL starts with "mailto:".');
      return false;
    }

    Uri? uri;
    try {
      uri = Uri.parse(url);
    } catch (e) {
      print('URL parsing failed: $e');
      return false;
    }

    if (uri.scheme.isEmpty || uri.host.isEmpty) {
      print('URL is missing a scheme (protocol) or host.');
      return false;
    }

    if (uri.hasAuthority &&
        uri.userInfo.contains(':') &&
        uri.userInfo.split(':').length > 2) {
      print('URL contains invalid user info.');
      return false;
    }

    if (uri.hasPort && (uri.port <= 0 || uri.port > 65535)) {
      print('URL contains an invalid port number.');
      return false;
    }

    print('URL is valid.');
    return true;
  }

  Future<bool> isValidGitHubRepo(String repoUrl) async {
    if (!isValidUrl(repoUrl)) return false;

    var uri = Uri.parse(repoUrl);
    if (uri.host != 'github.com') return false;

    var segments = uri.pathSegments;
    if (segments.length < 2) return false;

    var user = segments[0];
    var repo = segments[1];

    var apiUri = Uri.https('api.github.com', '/repos/$user/$repo');

    var response = await http.get(apiUri);
    if (response.statusCode != 200) return false;

    var data = json.decode(response.body);
    return data is Map && data['full_name'] == '$user/$repo';
  }
}
