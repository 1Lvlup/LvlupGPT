import Cocoa
import FlutterMacOS

// Define a MainFlutterWindow class that inherits from NSWindow
class MainFlutterWindow: NSWindow {
  
  // Override the awakeFromNib method to perform additional configuration
  override func awakeFromNib() {
    
    // Create a new FlutterViewController instance
    let flutterViewController = FlutterViewController()
    
    // Get the current window frame and set it as the frame for the FlutterViewController
    let windowFrame = self.frame
    self.contentViewController = flutterViewController
    self.setFrame(windowFrame, display: true)
    
    // Register any generated plugins with the FlutterViewController
    RegisterGeneratedPlugins(registry: flutterViewController)
    
    // Call the superclass's awakeFromNib method
    super.awakeFromNib()
  }
}
