import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_queue_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

// SideBarView is a StatelessWidget that displays a sidebar with various options.
class SideBarView extends StatelessWidget {
  // The constructor takes a required ValueNotifier<String> named selectedViewNotifier.
  const SideBarView({super.key, required this.selectedViewNotifier});

  // Function to launch the URL.
  void _launchURL(String urlString) async {
    // Parse the URL string into a Uri object.
    var url = Uri.parse(urlString);
    // Check if the URL can be launched.
    if (await canLaunchUrl(url)) {
      // Launch the URL.
      await launchUrl(url);
    } else {
      // Throw an error if the URL cannot be launched.
      throw 'Could not launch $url';
    }
  }

  // Function to create an IconButton for the menu items.
  Widget _menuItem(
    String title,
    String iconName,
    String viewName, {
    bool isDeveloperOnly = false,
    bool isBenchmarkRunning = false,
  }) {
    // Get the TaskQueueViewModel and SettingsViewModel instances from the context.
    final taskQueueViewModel =
        Provider.of<TaskQueueViewModel>(context, listen: true);
    final settingsViewModel =
        Provider.of<SettingsViewModel>(context, listen: true);

    // Return an IconButton widget.
    return IconButton(
      // Set the splash radius.
      splashRadius: 0.1,
      // Set the color of the IconButton based on the selected view.
      color: selectedViewNotifier.value == viewName
          ? Colors.blue
          : Colors.black,
      // Set the icon of the IconButton using an Image.asset widget.
      icon: Image.asset('assets/images/$iconName.png'),
      // Set the onPressed callback for the IconButton.
      onPressed: isBenchmarkRunning ||
              (isDeveloperOnly && !settingsViewModel.isDeveloperModeEnabled)
          ? null
          : () => selectedViewNotifier.value = viewName, // Update the selected view when the IconButton is pressed.
    );
  }

  @override
  Widget build(BuildContext context) {
    // Return a Material widget that wraps the entire SideBarView.
    return Material(
      // Set the child of the Material widget to a ValueListenableBuilder.
      child: ValueListenableBuilder(
          // Pass in the selectedViewNotifier as the valueListenable.
          valueListenable: selectedViewNotifier,
          // Build the UI based on the current value of the selectedViewNotifier.
          builder: (context, String selectedView, _) {
            // Return a SizedBox widget that wraps the entire SideBarView.
            return SizedBox(
              // Set the width of the SizedBox.
              width: 60,
              // Set the child of the SizedBox to a Column widget.
              child: Column(
                // Set the main axis alignment of the Column widget.
                children: [
                  // The first Column contains the main menu items.
                  Column(
                    children: [
                      // The TaskView menu item.
                      _menuItem('TaskView', 'chat', 'TaskView'),
                      // The SkillTreeView menu item, which is only visible if developer mode is enabled.
                      if (Provider.of<SettingsViewModel>(context, listen: true)
                          .isDeveloperModeEnabled)
                        _menuItem('SkillTreeView', 'emoji_events', 'SkillTreeView',
                            isDeveloperOnly: true),
                      // The SettingsView menu item.
                      _menuItem('SettingsView', 'settings', 'SettingsView'),
                    ],
                  ),
                  // Add a Spacer widget to push the bottom menu items to the bottom of the SideBarView.
                  const Spacer(),
                  // The bottom menu items.
                  Column(
                    children: [
                      // A GestureDetector widget that launches a URL when tapped.
                      GestureDetector(
                        // Set the onTap callback for the GestureDetector.
                        onTap: () =>
                            _launchURL('https://aiedge.medium.com/autogpt-forge-e3de53cc58ec'),
                        // Set the child of the GestureDetector to a Tooltip widget.
                        child: Tooltip(
                          // Set the message displayed by the Tooltip.
                          message: 'Learn how to build your own Agent',
                          // Set the child of the Tooltip to an Icon widget.
                          child: Icon(
                            Icons.book,
                            color: Color.fromRGBO(50, 120, 123, 1),
                            size: 25,
                          ),
                        ),
                      ),
                      // Another GestureDetector widget that launches a URL when tapped.
                      GestureDetector(
                        // Set the onTap callback for the GestureDetector.
                        onTap: () =>
                            _launchURL('https://leaderboard.agpt.co'),
                        // Set the child of the GestureDetector to a Tooltip widget.
                        child: Tooltip(
                          // Set the message displayed by the Tooltip.
                          message: 'Check out the leaderboard',
                          // Set the child of the Tooltip to an Image.asset widget.
                          child: Image.asset(
                            'assets/images/autogpt_logo.png',
                            width: 33,
                            height: 33,
                          ),
                        ),
                      ),
                      // Another GestureDetector widget
