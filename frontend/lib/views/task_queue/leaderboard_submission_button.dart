import 'package:auto\_gpt\_flutter\_client/constants/app\_colors.dart';
import 'package:flutter/material.dart';

/// A custom [StatelessWidget] for a leaderboard submission button.
///
/// This widget provides a disabled state and tooltip message when a user
/// attempts to submit to the leaderboard before completing a test suite.
class LeaderboardSubmissionButton extends StatelessWidget {
  /// The callback function to be called when the button is pressed.
  final VoidCallback? onPressed;

  /// A flag to determine if the button is disabled.
  final bool isDisabled;

  /// Constructor for the [LeaderboardSubmissionButton] widget.
  LeaderboardSubmissionButton({
    required this.onPressed,
    this.isDisabled = false,
  });

  @override
  Widget build(BuildContext context) {
    // The main button widget with custom styles.
    final button = SizedBox(
      height: 50,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          // Button background color based on disabled state.
          backgroundColor: isDisabled ? Colors.grey : AppColors.primaryLight,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8.0),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          elevation: 5.0,
        ),
        onPressed: isDisabled ? null : onPressed, // Callback function for onPressed.
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Submit to leaderboard', // The text displayed on the button.
              style: TextStyle(
                color: Colors.white,
                fontSize: 12.50,
                fontFamily: 'Archivo',
                fontWeight: FontWeight.w400,
              ),
            ),
            SizedBox(width: 10),
            Icon(
              Icons.emoji\_events, // The icon displayed on the button.
              color: Colors.white,
              size: 24,
            ),
          ],
        ),
      ),
    );

    // Tooltip displayed when the button is disabled.
    return isDisabled
        ? Tooltip(
            message:
                "You must complete a test suite before submitting to the leaderboard.", // Tooltip message.
            child: button,
          )
        : button;
  }
}
