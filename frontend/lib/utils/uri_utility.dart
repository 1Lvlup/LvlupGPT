import 'package:http/http.dart' as http;
import 'dart:convert';

/// A class that contains utility functions for handling URIs.
class UriUtility {
  /// Checks if the given URL is valid.
  ///
  /// [url] The URL to check.
  ///
  /// Returns `true` if the URL is valid, `false` otherwise.
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
      uri = Uri.parse(url); // Parse the URL into a Uri object
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

  /// Checks if the given GitHub repository URL is valid.
  ///
  /// [repoUrl] The GitHub repository URL to check.
  ///
  /// Returns `true` if the repository URL is valid, `false` otherwise.
  Future<bool> isValidGitHubRepo(String repoUrl) async {
    if (!isValidUrl(repoUrl)) return false; // Check if the URL is valid

    var uri = Uri.parse(repoUrl); // Parse the URL into a Uri object
    if (uri.host != 'github.com') return false; // Check if the host is github.com

    var segments = uri.pathSegments; // Get the path segments of the URL
    if (segments.length < 2) return false; // Check if there are at least two segments

    var user = segments[0]; // The first segment is the username
    var repo = segments[1]; // The second segment is the repository name

    var apiUri = Uri.https
