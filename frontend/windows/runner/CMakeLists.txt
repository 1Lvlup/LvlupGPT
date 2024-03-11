# cmake_minimum_required(VERSION 3.14)
# 
# Sets the minimum version of CMake required to build this project.
# In this case, version 3.14 or higher is required.

project(runner LANGUAGES CXX)

# Define the application target and include its source files.
add_executable(
  ${BINARY_NAME}  # The name of the executable target, generated from the project name.
  WIN32            # Specifies that this is a Windows application.
  "flutter_window.cpp"
  "main.cpp"
  "utils.cpp"
  "win32_window.cpp"
  "${FLUTTER_MANAGED_DIR}/generated_plugin_registrant.cc"
  "Runner.rc"
  "runner.exe.manifest"
)

# Apply the standard set of build settings and add preprocessor definitions.
include(StandardBuildSettings)
standard_build_settings(${BINARY_NAME})

# The following target_compile_definitions() commands add preprocessor definitions
# specific to the Flutter version and platform.
target_compile_definitions(
  ${BINARY_NAME}
  PRIVATE "FLUTTER_VERSION=${FLUTTER_VERSION}"
  PRIVATE "FLUTTER_VERSION_MAJOR=${FLUTTER_VERSION_MAJOR}"
  PRIVATE "FLUTTER_VERSION_MINOR=${FLUTTER_VERSION_MINOR}"
  PRIVATE "FLUTTER_VERSION_PATCH=${FLUTTER_VERSION_PATCH}"
  PRIVATE "FLUTTER_VERSION_BUILD=${FLUTTER_VERSION_BUILD}"
)

# Disable Windows macros that collide with C++ standard library functions.
target_compile_definitions(${BINARY_NAME} PRIVATE "NOMINMAX")

# Add dependency libraries and include directories.
target_link_libraries(
  ${BINARY_NAME}
  PRIVATE flutter
  PRIVATE flutter_wrapper_app
  PRIVATE "dwmapi.lib"
)
target_include_directories(${BINARY_NAME} PRIVATE "${CMAKE_SOURCE_DIR}")

# Run the Flutter tool portions of the build.
add_dependencies(${BINARY_NAME} flutter_assem
