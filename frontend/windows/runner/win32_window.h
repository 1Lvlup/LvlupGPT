// Win32Window.h: A high DPI-aware Win32 Window abstraction class
// 
// This class serves as an abstraction for a high DPI-aware Win32 Window. It is
// intended to be inherited from by classes that wish to specialize with custom
// rendering and input handling.

#ifndef RUNNER_WIN32_WINDOW_H_
#define RUNNER_WIN32_WINDOW_H_

#include <windows.h> // Include Windows.h for Win32 API

#include <functional>
#include <memory>
#include <string>

// Point struct: Represents a point in the window with x and y coordinates
struct Win32Window::Point {
  unsigned int x;
  unsigned int y;
  Point(unsigned int x, unsigned int y) : x(x), y(y) {}
};

// Size struct: Represents the width and height of the window
struct Win32Window::Size {
  unsigned int width;
  unsigned int height;
  Size(unsigned int width, unsigned int height)
      : width(width), height(height) {}
};

// Win32Window class: A high DPI-aware Win32 Window
class Win32Window {
 public:
  // Default constructor
  Win32Window();

  // Destructor
  virtual ~Win32Window();

  // Creates a win32 window with the given title, origin, and size. The window
  // is invisible until Show() is called. Returns true if the window was
  // created successfully.
  bool Create(const std::wstring& title, const Point& origin, const Size& size);

  // Shows the current window. Returns true if the window was successfully shown.
  bool Show();

  // Releases OS resources associated with the window.
  void Destroy();

  // Inserts content into the window tree.
  void SetChildContent(HWND content);

  // Returns the backing Window handle to enable clients to set icon and other
  // window properties. Returns nullptr if the window has been destroyed.
  HWND GetHandle();

  // If true, closing this window will quit the application.
  void SetQuitOnClose(bool quit_on_close);

  // Returns a RECT representing the bounds of the current client area.
  RECT GetClientArea();

 protected:
  // Processes and routes salient window messages for mouse handling, size
  // change, and DPI. Delegates handling of these to member overloads that
  // inheriting classes can handle.
  virtual LRESULT MessageHandler(HWND window,
                                 UINT const message,
                                 WPARAM const wparam,
                                 LPARAM const lparam) noexcept;

  // Called when CreateAndShow is called, allowing subclass window-related
  // setup. Subclasses should return false if setup fails.
  virtual bool OnCreate();

  // Called when Destroy is called.
  virtual void OnDestroy();

 private:
  friend class WindowClassRegistrar;

  // OS callback called by message pump. Handles the WM_NCCREATE message which
  // is passed when the non-client area is being created and enables automatic
  // non-client DPI scaling so that the non-client area automatically
  // responds to changes in DPI. All other messages are handled by
  // MessageHandler.
  static LRESULT CALLBACK WndProc(HWND const window,
                                  UINT const message,
                                  WPARAM const wparam,
                                  LPARAM const lparam) noexcept;

  // Retrieves a class instance pointer for |window|
  static Win32Window* GetThisFromHandle(HWND const window) noexcept;

  // Update the window frame's theme to match the system theme.
  static void UpdateTheme(HWND const window);

  bool quit_on_close_ = false;

  // window handle for top level window.
  HWND window_handle_ = nullptr;

  // window handle for hosted content.
  HWND child_content_ = nullptr;
};

#endif  // RUNNER_WIN32_WINDOW_H_
