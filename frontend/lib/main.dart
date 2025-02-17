import 'package:auto_gpt_flutter_client/services/leaderboard_service.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_queue_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/auth/firebase_auth_view.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/skill_tree_viewmodel.dart';
import 'package:auto_gpt_flutter_client/services/chat_service.dart';
import 'package:auto_gpt_flutter_client/services/task_service.dart';
import 'package:auto_gpt_flutter_client/services/benchmark_service.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  runApp(
    MultiProvider(
      providers: [
        Provider(
          create: (_) => RestApiUtility("http://127.0.0.1:8000/ap/v1"),
        ),
        Provider(
          create: (_) => SharedPreferencesService.instance,
        ),
        ProxyProvider<RestApiUtility, ChatService>(
          update: (context, restApiUtility, chatService) =>
              ChatService(restApiUtility),
        ),
        ProxyProvider2<RestApiUtility, SharedPreferencesService, TaskService>(
          update: (context, restApiUtility, prefsService, taskService) =>
              TaskService(restApiUtility, prefsService),
        ),
        ProxyProvider<RestApiUtility, BenchmarkService>(
          update: (context, restApiUtility, benchmarkService) =>
              BenchmarkService(restApiUtility),
        ),
        ProxyProvider<RestApiUtility, LeaderboardService>(
          update: (context, restApiUtility, leaderboardService) =>
              LeaderboardService(restApiUtility),
        ),
        ChangeNotifierProxyProvider2<RestApiUtility, SharedPreferencesService,
            SettingsViewModel>(
          create: (context) => SettingsViewModel(
            Provider.of<RestApiUtility>(context, listen: false),
            Provider.of<SharedPreferencesService>(context, listen: false),
          ),
          update: (context, restApiUtility, prefsService, settingsViewModel) =>
              SettingsViewModel(restApiUtility, prefsService),
        ),
        ChangeNotifierProvider(
          create: (context) => TaskViewModel(
            Provider.of<TaskService>(context, listen: false),
            Provider.of<SharedPreferencesService>(context, listen: false),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => ChatViewModel(
            Provider.of<ChatService>(context, listen: false),
            Provider.of<SharedPreferencesService>(context, listen: false),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => SkillTreeViewModel(),
        ),
        ChangeNotifierProvider(
          create: (context) => TaskQueueViewModel(
            Provider.of<BenchmarkService>(context, listen: false),
            Provider.of<LeaderboardService>(context, listen: false),
            Provider.of<SharedPreferencesService>(context, listen: false),
          ),
        ),
      ],
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final taskService = Provider.of<TaskService>(context, listen: false);
    taskService.loadDeletedTasks();

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AutoGPT Flutter Client',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: StreamBuilder<User?>(
        stream: FirebaseAuth.instance.authStateChanges(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator();
          }
          if (snapshot.hasData && snapshot.data != null) {
            return MultiProvider(
              providers: [
                ChangeNotifierProvider(
                  create: (context) => TaskQueueViewModel(
                    Provider.of<BenchmarkService>(context, listen: false),
                    Provider.of<LeaderboardService>(context, listen: false),
                    Provider.of<SharedPreferencesService>(context,
                        listen: false),
                  ),
                ),
              ],
              child: MainLayout(),
            );
          }
          return FirebaseAuthView();
        },
      ),
    );
  }
}
