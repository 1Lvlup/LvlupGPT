#include <windows.h> // Include header for Windows API
#include <dwmapi.h>  // Include header for DWM (Desktop Window Manager) API
#include <flutter_windows.h> // Include header for Flutter Windows API
#include <string>          // Include header for std::string
#include <vector>          // Include header for std::vector

#include "win32_window.h"   // Include header for this translation unit

namespace { // Anonymous namespace for local helper functions

constexpr const wchar_t kWindowClassName[] = L"FLUTTER_RUNNER_WIN32_WINDOW";
constexpr const wchar_t kGetPreferredBrightnessRegKey[] =
  L"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize";
constexpr const wchar_t kGetPreferredBrightnessRegValue[] = L"AppsUseLightTheme";

// The number of Win32Window objects that currently exist.
static int g_active_window_count = 0;

// Scale helper to convert logical scaler values to physical using passed in
// scale factor
int Scale(int source, double scale_factor) {
  return static_cast<int>(source * scale_factor); // Scale the source value by the scale factor
}

// Dynamically loads the |EnableNonClientDpiScaling| from the User32 module.
// This API is only needed for PerMonitor V1 awareness mode.
void EnableFullDpiSupportIfAvailable(HWND hwnd) {
  HMODULE user32_module = LoadLibraryA("User32.dll"); // Load User32.dll
  if (!user32_module) { // Check if the module was loaded successfully
    return;
  }
  auto enable_non_client_dpi_scaling =
      reinterpret_cast<EnableNonClientDpiScaling*>(
          GetProcAddress(user32_module, "EnableNonClientDpiScaling"));
  if (enable_non_client_dpi_scaling != nullptr) { // Check if the API was found
    enable_non_client_dpi_scaling(hwnd); // Enable non-client DPI scaling
  }
  FreeLibrary(user32_module); // Free the loaded module
}

class WindowClassRegistrar { // Class to register and unregister window class
 public:
  ~WindowClassRegistrar() = default;

  // Returns the singleton registrar instance.
  static WindowClassRegistrar* GetInstance() {
    if (!instance_) { // Create the instance if it doesn't exist
      instance_ = new WindowClassRegistrar();
    }
    return instance_;
  }

  // Returns the name of the window class, registering the class if it hasn't
  // previously been registered.
  const wchar_t* GetWindowClass();

  // Unregisters the window class. Should only be called if there are no
  // instances of the window.
  void UnregisterWindowClass();

 private:
  WindowClassRegistrar() = default;

  static WindowClassRegistrar* instance_;

  bool class_registered_ = false;

  WNDCLASS window_class_;
};

WindowClassRegistrar* WindowClassRegistrar::instance_ = nullptr;

const wchar_t* WindowClassRegistrar::GetWindowClass() {
  if (!class_registered_) { // Register the window class if it hasn't been registered
    window_class_.hCursor = LoadCursor(nullptr, IDC_ARROW);
    window_class_.lpszClassName = kWindowClassName;
    window_class_.style = CS_HREDRAW | CS_VREDRAW;
    window_class_.cbClsExtra = 0;
    window_class_.cbWndExtra = 0;
    window_class_.hInstance = GetModuleHandle(nullptr);
    window_class_.hIcon =
        LoadIcon(window_class_.hInstance, MAKEINTRESOURCE(IDI_APP_ICON));
    window_class_.hbrBackground = 0;
    window_class_.lpszMenuName = nullptr;
    window_class_.lpfnWndProc = Win32Window::WndProc;
    RegisterClass(&window_class_);
    class_registered_ = true;
  }
  return kWindowClassName;
}

void WindowClassRegistrar::UnregisterWindowClass() {
  UnregisterClass(kWindowClassName, nullptr); // Unregister the window class
  class_registered_ = false;
}

Win32Window::Win32Window() {
  ++g_active_window_count; // Increment the active window count
}

Win32Window::~Win32Window() {
  --g_active_window_count; // Decrement the active window count
  Destroy();
}

bool Win32Window::Create(const std::wstring& title,
                         const Point& origin,
                         const Size& size) {
  Destroy(); // Destroy any existing window

  const wchar_t* window_class =
      WindowClassRegistrar::GetInstance()->GetWindowClass(); // Get the window class

  const POINT target_point = {static_cast<LONG>(origin.x),
                              static_cast<LONG>(origin.y)};
  HMONITOR monitor = MonitorFromPoint(target_point, MONITOR_DEFAULTTONEAREST); // Get the monitor that contains the target point
  UINT dpi = FlutterDesktopGetDpiForMonitor(monitor); // Get the DPI for the monitor
  double scale_factor = dpi / 96.0; // Calculate the scale factor

  HWND window = CreateWindow(
      const_cast<wchar_t*>(window_class), title.c_str(), WS_OVERLAPPEDWINDOW,
      Scale(origin.x, scale_factor), Scale(origin.y, scale_factor),
      Scale(size.width, scale_factor), Scale(size.height, scale_factor),
      nullptr, nullptr, window_class_.hInstance, this); // Create the window

  if (!window) { // Check if the window was created successfully
   
