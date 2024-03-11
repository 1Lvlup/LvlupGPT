import Cocoa
import FlutterMacOS

@main
class AppDelegate: FlutterAppDelegate {
    override func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        // Return true to allow the application to terminate after the last window is closed
        // Return false if you want the application to continue running even after the last window is closed
        return true
    }
    
    override func configureFlutterEngine(_ engine: FlutterEngine) {
        super.configureFlutterEngine(engine)
        
        // Configure additional Flutter engine settings here, if needed
    }
}
