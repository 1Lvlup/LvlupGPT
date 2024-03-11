import 'package:auto_gpt_flutter_client/services/auth_service.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final settingsViewModelProvider =
    ChangeNotifierProvider<SettingsViewModel>((ref) {
  final restApiUtility = ref.watch(restApiUtilityProvider);
  final prefsService = ref.watch(sharedPreferencesServiceProvider);
  return SettingsViewModel(restApiUtility, prefsService);
});

final restApiUtilityProvider = Provider<RestApiUtility>((ref) {
  return RestApiUtility();
});

final sharedPreferencesServiceProvider =
    Provider<SharedPreferencesService>((ref) {
  return SharedPreferencesService();
});

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService();
});

class SettingsViewModel extends ChangeNotifier {
  bool _isDarkModeEnabled = false;
  bool _isDeveloperModeEnabled = false;
  String _baseURL = '';
  int _continuousModeSteps = 1;

  late RestApiUtility _restApiUtility;
  late SharedPreferencesService _prefsService;
  late AuthService _authService;

  SettingsViewModel(this._restApiUtility, this._prefsService) {
    _authService = ref.read(authServiceProvider);
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    _isDarkModeEnabled =
        await _prefsService.getBool('isDarkModeEnabled') ?? false;
    _isDeveloperModeEnabled =
        await _prefsService.getBool('isDeveloperModeEnabled') ?? true;
    _baseURL = await _prefsService.getString('baseURL') ??
        'http://127.0.0.1:8000/ap/v1';
    _restApiUtility.updateBaseURL(_baseURL);
    _continuousModeSteps =
        await _prefsService.getInt('continuousModeSteps') ?? 10;
    notifyListeners();
  }

  //... Rest of the class remains the same
}
