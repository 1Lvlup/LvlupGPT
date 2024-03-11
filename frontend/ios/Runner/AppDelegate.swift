import UIKit
import Flutter
import Firebase

// The main AppDelegate class for the application
@UIApplicationMain
class AppDelegate: FlutterAppDelegate {
  // Called when the application finishes launching
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    // Initialize Firebase before registering plugins
    FirebaseApp.configure()

    do {
      // Register plugins after Firebase initialization
      try GeneratedPluginRegistrant.register(with: self)
      // Call the superclass method to continue with the launch process
      return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    } catch {
      // Handle any errors that occur during plugin registration
      print("Error registering plugins: \(error)")
      return false
    }
  }
}

