#ifndef RUNNER_FLUTTER_WINDOW_H_
#define RUNNER_FLUTTER_WINDOW_H_

#include <flutter/dart_project.h>  // Include the DartProject header from Flutter SDK
#include <flutter/flutter_view_controller.h>  // Include the FlutterViewController header from Flutter SDK

#include <memory>  // Include the standard memory header for unique_ptr

#include "win32_window.h"  // Include the Win32Window header

// ----------------------------------------------------------------------------
// FlutterWindow: A window that hosts a Flutter view
// ----------------------------------------------------------------------------
class FlutterWindow : public Win32Window {
 public:
  // -------------------------------------------------------------------------
  // Constructor: Creates a new FlutterWindow hosting a Flutter view running |project|
  // -------------------------------------------------------------------------
  explicit FlutterWindow(const flutter::DartProject& project);

  // -------------------------------------------------------------------------
  // Destructor: Virtual to ensure proper destruction of derived objects
  // -------------------------------------------------------------------------
  virtual ~FlutterWindow();

 protected:
  // Win32Window:

  // -------------------------------------------------------------------------
  // OnCreate: Called when the window is created
  // -------------------------------------------------------------------------
  bool OnCreate() override;

  // -------------------------------------------------------------------------
  // OnDestroy: Called when the window is about to be destroyed
  // -------------------------------------------------------------------------
  void OnDestroy() override;

  // -------------------------------------------------------------------------
  // MessageHandler: Handles messages sent to the window
  // -------------------------------------------------------------------------
  LRESULT MessageHandler(HWND window, UINT const message, WPARAM const wparam,
                         LPARAM const lparam) noexcept override;

 private:
  // The project to run
  flutter::DartProject project_;

  // The Flutter instance hosted by this window
  std::unique_ptr<flutter::FlutterViewController> flutter_controller_;
};

