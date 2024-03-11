import 'package:shared_preferences/shared_preferences.dart';

/// A singleton service for managing shared preferences across the application.
class SharedPreferencesService {
  /// The private constructor to enforce the singleton pattern.
  SharedPreferencesService._privateConstructor();

  /// The singleton instance of the SharedPreferencesService.
  static final SharedPreferencesService instance =
      SharedPreferencesService._privateConstructor();

  /// The shared preferences instance, initialized lazily upon the first call to [initialize].
  late SharedPreferences _prefs;

  /// Initializes the shared preferences instance.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<void> initialize() async => _prefs = await SharedPreferences.getInstance();

  /// Saves a boolean value to the shared preferences using the given key.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<void> setBool(String key, bool value) async => _prefs.setBool(key, value);

  /// Saves a string value to the shared preferences using the given key.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<void> setString(String key, String value) async => _prefs.setString(key, value);

  /// Saves an integer value to the shared preferences using the given key.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<void> setInt(String key, int value) async => _prefs.setInt(key, value);

  /// Saves a list of strings to the shared preferences using the given key.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<void> setStringList(String key, List<String> value) async => _prefs.setStringList(key, value);

  /// Retrieves a boolean value from the shared preferences using the given key.
  ///
  /// This method is asynchronous and should be awaited when called.
  Future<bool
