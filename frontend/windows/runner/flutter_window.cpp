// Include necessary headers for Flutter window creation and management.
#include "flutter_window.h"

// Include optional header for using std::optional.
#include <optional>

// Include Flutter headers for generating plugin registrant and initializing
// Flutter engine.
#include "flutter/generated_plugin_registrant.h"

// Constructor for FlutterWindow class, initializing the project_ member.
FlutterWindow::FlutterWindow(const flutter::DartProject& project)
    : project_(project) {}

// Destructor for FlutterWindow class, cleaning up any resources.
FlutterWindow::~FlutterWindow() {}

// Overridden OnCreate() method for Win32Window, initializing the Flutter
// controller and setting up the window content.
bool FlutterWindow::OnCreate() {
  // Call the base class's OnCreate() method to initialize the window.
  if (!Win32Window::OnCreate()) {
    return false;
  }

  // Get the client area of the window to determine the frame size.
  RECT frame = GetClientArea();

  // Create a new FlutterViewController with the frame size and project.
  flutter_controller_ = std::make_unique<flutter::FlutterViewController>(
      frame.right - frame.left, frame.bottom - frame.top, project_);

  // Ensure that the engine and view of the controller are initialized.
  if (!flutter_controller_->engine() || !flutter_controller_->view()) {
    return false;
  }

  // Register plugins for the Flutter engine.
  RegisterPlugins(flutter_controller_->engine());

  // Set the child content of the window to the native window of the Flutter view.
  SetChildContent(flutter_controller_->view()->GetNativeWindow());

  // Schedule a frame to be rendered and show the window when ready.
  flutter_controller_->engine()->SetNextFrameCallback([&]() {
    this->Show();
  });

  return true;
}

// Overridden OnDestroy() method for Win32Window, cleaning up the Flutter
// controller.
void FlutterWindow::OnDestroy() {
  // Reset the Flutter controller pointer to release any resources.
  flutter_controller_ = nullptr;

  // Call the base class's OnDestroy() method to clean up the window.
  Win32Window::OnDestroy();
}

// Overridden MessageHandler() method for Win32Window, handling window messages
// and delegating them to the Flutter controller if necessary.
LRESULT
FlutterWindow::MessageHandler(HWND hwnd, UINT const message,
                              WPARAM const wparam,
                              LPARAM const lparam) noexcept {
  // If the Flutter controller is available, try to handle the message using
  // Flutter's message handling mechanism.
  if (flutter_controller_) {
    std::optional<LRESULT> result =
        flutter_controller_->HandleTopLevelWindowProc(hwnd, message, wparam,
                                                      lparam);
    if
