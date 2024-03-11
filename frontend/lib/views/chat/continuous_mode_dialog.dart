import 'package:auto\_gpt\_flutter\_client/constants/app\_colors.dart';
import 'package:flutter/material.dart';

/// A dialog that appears when the user attempts to dismiss the continuous mode dialog.
/// It informs the user that they cannot dismiss the dialog and provides a red exclamation mark icon.
class ContinuousModeDialog extends StatefulWidget {
// Constructor for ContinuousModeDialog, which takes several parameters:
// - onProceed: A callback function that is called when the user taps the "Proceed" button.
// - onCheckboxChanged: A callback function that is called when the user toggles the "Don't ask again" checkbox.
// - title: The title of the dialog.
// - content: The main content of the dialog.
// - proceedButtonText: The text for the "Proceed" button.
// - cancelButtonText: The text for the "Cancel" button.
  const ContinuousModeDialog({
    Key? key,
    this.onProceed,
    this.onCheckboxChanged,
    required this.title,
    required this.content,
    this.proceedButtonText = 'Proceed',
    this.cancelButtonText = 'Cancel',
  }) : super(key: key);

  @override
  _ContinuousModeDialogState createState() => _ContinuousModeDialogState();
}

/// State for the ContinuousModeDialog widget.
class _ContinuousModeDialogState extends State<ContinuousModeDialog> {
  bool _attemptedToDismiss = false; // Tracks whether the user has attempted to dismiss the dialog.
  bool _checkboxValue = false; // Tracks the value of the "Don't ask again" checkbox.

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      // Prevents the user from dismissing the dialog by pressing the back button.
      onWillPop: () async {
        setState(() {
          _attemptedToDismiss = true;
        });
        return false;
      },
      child: Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8.0),
          side: BorderSide(
            color: _attemptedToDismiss
                ? AppColors.accentDeniedLight
                : Colors.transparent,
            width: 3.0,
          ),
        ),
        child: Container(
          width: 260,
          height: 251,
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              // Black circle exclamation icon
              Icon(
                Icons.error_outline,
                color: _attemptedToDismiss
                    ? AppColors.accentDeniedLight
                    : Colors.black,
              ),
              const SizedBox(height: 8),
              // Title
              Text(
                widget.title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 16,
                  fontFamily: 'Archivo',
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              // Block of text
              SizedBox(
                width: 220,
                child: Text(
                  widget.content,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 12.50,
                    fontFamily: 'Archivo',
                    fontWeight: FontWeight.w400,
                  ),
                ),
              ),
              const SizedBox(height: 14),
              // Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Cancel Button
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.grey,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8.0),
                      ),
                    ),
                    onPressed: () => Navigator.of(context).pop(),
                    child: Text(
                      widget.cancelButtonText,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12.50,
                        fontFamily: 'Archivo',
                        fontWeight: FontWeight.w400,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Proceed Button
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryLight,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8.0),
                      ),
                    ),
                    onPressed: widget.onProceed, // Use the provided callback
                    child: Text(
                      widget.proceedButtonText,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12.50,
                        fontFamily: 'Archivo',
                        fontWeight: FontWeight.w400,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 11),
              // Checkbox and text
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Checkbox(
                    value: _checkboxValue,
                    onChanged: (bool? newValue) {
                      setState(() {
                        _checkboxValue = newValue ?? false;
                      });
                      if (widget.onCheckboxChanged != null) {
                        widget.onCheckboxChanged!(_checkboxValue);
                      }
                    },
                  ),
                  const Text(
                    "
