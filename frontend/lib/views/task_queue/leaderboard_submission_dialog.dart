import 'package:auto_gpt_flutter_client/constants/app_colors.dart';
import 'package:auto_gpt_flutter_client/utils/uri_utility.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_queue_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// This class represents the LeaderboardSubmissionDialog widget, which is a
/// dialog for submitting a leaderboard entry with team name, GitHub repo URL,
/// and commit SHA.
class LeaderboardSubmissionDialog extends StatefulWidget {
  /// Constructor for the LeaderboardSubmissionDialog widget.
  ///
  /// onSubmit: A callback function that is called when the submission is
  ///   valid and the user presses the submit button. It takes three string
  ///   parameters: teamName, repoUrl, and commitSha.
  /// viewModel: The TaskQueueViewModel instance that is used for shared
  ///   preferences operations.
  const LeaderboardSubmissionDialog({
    Key? key,
    this.onSubmit,
    required this.viewModel,
  }) : super(key: key);

  /// The TaskQueueViewModel instance that is used for shared preferences
  /// operations.
  final TaskQueueViewModel viewModel;

  @override
  _LeaderboardSubmissionDialogState createState() =>
      _LeaderboardSubmissionDialogState();
}

/// This class represents the state of the LeaderboardSubmissionDialog widget.
class _LeaderboardSubmissionDialogState extends State<LeaderboardSubmissionDialog> {
  /// The TextEditingController for the team name input field.
  final TextEditingController _teamNameController = TextEditingController();

  /// The TextEditingController for the GitHub repo URL input field.
  final TextEditingController _repoUrlController = TextEditingController();

  /// The TextEditingController for the commit SHA input field.
  final TextEditingController _commitShaController = TextEditingController();

  /// The error message for the team name input field.
  String? _teamNameError;

  /// The error message for the GitHub repo URL input field.
  String? _repoUrlError;

  /// The error message for the commit SHA input field.
  String? _commitShaError;

  @override
  void initState() {
    super.initState();
    _initSharedPreferences();
  }

  /// Initializes shared preferences by getting stored values for team name,
  /// GitHub repo URL, and commit SHA.
  Future<void> _initSharedPreferences() async {
    // Using the SharedPreferencesService from the viewModel to get stored values
    _teamNameController.text =
        await widget.viewModel.prefsService.getString('teamName') ?? '';
    _repoUrlController.text =
        await widget.viewModel.prefsService.getString('repoUrl') ?? '';
    _commitShaController.text =
        await widget.viewModel.prefsService.getString('commitSha') ?? '';
  }

  /// Validates the input fields and submits the leaderboard entry if the input
  /// is valid.
  void _validateAndSubmit() async {
    setState(() {
      _teamNameError = null;
      _repoUrlError = null;
      _commitShaError = null;
    });

    bool isValid = true;

    if (_teamNameController.text.isEmpty) {
      isValid = false;
      _teamNameError = 'Team Name is required';
    }

    if (_repoUrlController.text.isEmpty) {
      isValid = false;
      _repoUrlError = 'Repo URL is required';
    } else if (!UriUtility.isURL(_repoUrlController.text)) {
      isValid = false;
      _repoUrlError = 'Invalid URL format';
    } else if (!(await UriUtility()
        .isValidGitHubRepo(_repoUrlController.text))) {
      isValid = false;
      _repoUrlError = 'Not a valid GitHub repository';
    }

    if (_commitShaController.text.isEmpty) {
      isValid = false;
      _commitShaError = 'Commit SHA is required';
    }

    if (isValid) {
      print('Valid leaderboard submission parameters!');
      await _saveToSharedPreferences();
      widget.onSubmit?.call(_teamNameController.text, _repoUrlController.text,
          _commitShaController.text);
      Navigator.of(context).pop();
    } else {
      setState(() {});
    }
  }

  /// Saves the input field values to shared preferences.
  Future<void> _saveToSharedPreferences() async {
    // Using the prefsService to save the values
    await widget.viewModel.prefsService
        .setString('teamName', _teamNameController.text);
    await widget.viewModel.prefsService
        .setString('repoUrl', _repoUrlController.text);
    await widget.viewModel.prefsService
        .setString('commitSha', _commitShaController.text);
  }

  @override
  Widget build(BuildContext context) {
    final containerHeight = 324.0 +
        (_teamNameError == null ? 0 : 22) +
        (_repoUrlError == null ? 0 : 22) +
        (_commitShaError == null ? 0 : 22);
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: Container(
        width: 260,
        height: containerHeight,
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title
            const Text(
              'Leaderboard Submission',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.black,
                fontSize: 16,
                fontFamily: 'Archivo',
                font
