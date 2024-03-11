#include <flutter/dart_project.h>
#include <flutter/flutter_view_controller.h>
#include <windows.h>

#include "flutter_window.h"
#include "utils.h"

// The entry point for the Windows application. This function is called when
// the application starts.
int APIENTRY wWinMain(_In_ HINSTANCE instance, _In_opt_ HINSTANCE prev,
                      _In_ wchar_t *command_line, _In_ int show_command) {
  // Attach to console when present (e.g., 'flutter run') or create a new
  // console when running with a debugger.
  if (!::AttachConsole(ATTACH_PARENT_PROCESS) && ::IsDebuggerPresent()) {
    CreateAndAttachConsole();
  }

  // Initialize COM, so that it is available for use in the library and/or
  // plugins.
  ::CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);

  // Create a new DartProject object with the specified data directory.
  flutter::DartProject project(L"data");

  // Parse the command line arguments and set them as the Dart entrypoint
  // arguments for the project.
  std::vector<std::string> command_line_arguments =
      GetCommandLineArguments();
  project.set_dart_entrypoint_arguments(std::move(command_line_arguments));

  // Create a new FlutterWindow object with the specified project.
  FlutterWindow window(project);

  // Set the origin and size of the window.
  Win32Window::Point origin(10, 10);
  Win32Window::Size size(1280, 720);

  // Create the window with the specified title, origin, and size.
  if (!window.Create(L"auto_gpt_flutter_client", origin, size)) {
    return EXIT_FAILURE;
  }

  // Set the window to quit when closed.
  window.SetQuitOnClose(
