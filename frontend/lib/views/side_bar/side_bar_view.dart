import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_queue_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

class SideBarView extends StatelessWidget {
  final ValueNotifier<String> selectedViewNotifier;

  const SideBarView({super.key, required this.selectedViewNotifier});

  // Function to launch the URL
  void _launchURL(String urlString) async {
    var url = Uri.parse(urlString);
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  // Function to create an IconButton for the menu items
  Widget _menuItem(
    String title,
    String iconName,
    String viewName, {
    bool isDeveloperOnly = false,
    bool isBenchmarkRunning = false,
  }) {
    final taskQueueViewModel =
        Provider.of<TaskQueueViewModel>(context, listen: true);
    final settingsViewModel =
        Provider.of<SettingsViewModel>(context, listen: true);

    return IconButton(
      splashRadius: 0.1,
      color: selectedViewNotifier.value == viewName
          ? Colors.blue
          : Colors.black,
      icon: Image.asset('assets/images/$iconName.png'),
      onPressed: isBenchmarkRunning ||
              (isDeveloperOnly && !settingsViewModel.isDeveloperModeEnabled)
          ? null
          : () => selectedViewNotifier.value = viewName,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      child: ValueListenableBuilder(
          valueListenable: selectedViewNotifier,
          builder: (context, String selectedView, _) {
            return SizedBox(
              width: 60,
              child: Column(
                children: [
                  Column(
                    children: [
                      _menuItem('TaskView', 'chat', 'TaskView'),
                      if (Provider.of<SettingsViewModel>(context, listen: true)
                          .isDeveloperModeEnabled)
                        _menuItem('SkillTreeView', 'emoji_events', 'SkillTreeView',
                            isDeveloperOnly: true),
                      _menuItem('SettingsView', 'settings', 'SettingsView'),
                    ],
                  ),
                  const Spacer(),
                  Column(
                    children: [
                      GestureDetector(
                        onTap: () =>
                            _launchURL('https://aiedge.medium.com/autogpt-forge-e3de53cc58ec'),
                        child: Tooltip(
                          message: 'Learn how to build your own Agent',
                          child: Icon(
                            Icons.book,
                            color: Color.fromRGBO(50, 120, 123, 1),
                            size: 25,
                          ),
                        ),
                      ),
                      GestureDetector(
                        onTap: () =>
                            _launchURL('https://leaderboard.agpt.co'),
                        child: Tooltip(
                          message: 'Check out the leaderboard',
                          child: Image.asset(
                            'assets/images/autogpt_logo.png',
                            width: 33,
                            height: 33,
                          ),
                        ),
                      ),
                      GestureDetector(
                        onTap: () =>
                            _launchURL('https://discord.gg/autogpt'),
                        child: Tooltip(
                          message: 'Join our Discord',
                          child: Image.asset(
                            'assets/images/discord_logo.png',
                            width: 25,
                            height: 25,
                          ),
                        ),
                      ),
                      const SizedBox(height: 6),
                      Image.asset(
                        'assets/images/twitter_logo.png',
                        width: 15,
                        height: 15,
                      ),
                      const SizedBox(height: 8),
                    ],
                  ),
                ],
              ),
            );
          }),
    );
  }
}
