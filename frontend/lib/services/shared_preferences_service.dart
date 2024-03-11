import 'package:shared_preferences/shared_preferences.dart';

class SharedPreferencesService {
  SharedPreferencesService._privateConstructor();

  static final SharedPreferencesService instance =
      SharedPreferencesService._privateConstructor();

  late SharedPreferences _prefs;

  Future<void> initialize() async => _prefs = await SharedPreferences.getInstance();

  Future<void> setBool(String key, bool value) async => _prefs.setBool(key, value);

  Future<void> setString(String key, String value) async => _prefs.setString(key, value);

  Future<void> setInt(String key, int value) async => _prefs.setInt(key, value);

  Future<void> setStringList(String key, List<String> value) async => _prefs.setStringList(key, value);

  Future<bool?> getBool(String key) async => _prefs.getBool(key);

  Future<String?> getString(String key) async => _prefs.getString(key);

  Future<int?> getInt(String key) async => _prefs.getInt(key);

  Future<List<String>?> getStringList(String key) async => _prefs.getStringList(key);
}
