# This file controls Flutter-level build steps. It should not be edited.

cmake_minimum_required(VERSION 3.10)

set(EPHEMERAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/ephemeral")

# Configuration provided via flutter tool.
include(${EPHEMERAL_DIR}/generated_config.cmake)

# Serves the same purpose as list(TRANSFORM ... PREPEND ...),
# which isn't available in 3.10.
function(list_prepend LIST_NAME PREFIX)
    set(NEW_LIST "")
    foreach(element ${${LIST_NAME}})
        list(APPEND NEW_LIST "${PREFIX}${element}")
    endforeach(element)
    set(${LIST_NAME} "${NEW_LIST}" PARENT_SCOPE)
endfunction()

# === Flutter Library ===
# System-level dependencies.
find_package(PkgConfig REQUIRED)

set(GTK_REQUIRED_VARS)
if(NOT PkgConfig_FOUND)
    set(GTK_REQUIRED_VARS "PKG_CONFIG_EXECUTABLE")
endif()
pkg_check_modules(GTK REQUIRED ${GTK_REQUIRED_VARS} gtk+-3.0)

set(GLIB_REQUIRED_VARS)
if(NOT PkgConfig_FOUND)
    set(GLIB_REQUIRED_VARS "PKG_CONFIG_EXECUTABLE")
endif()
pkg_check_modules(GLIB REQUIRED ${GLIB_REQUIRED_VARS} glib-2.0)

set(GIO_REQUIRED_VARS)
if(NOT PkgConfig_FOUND)
    set(GIO_REQUIRED_VARS "PKG_CONFIG_EXECUTABLE")
endif()
pkg_check_modules(GIO REQUIRED ${GIO_REQUIRED_VARS} gio-2.0)

find_library(FLUTTER_LIBRARY NAME flutter_linux_gtk HINTS ${EPHEMERAL_DIR})
if(NOT FLUTTER_LIBRARY)
    message(FATAL_ERROR "Flutter library not found")
endif()

# Published to parent scope for install step.
set(FLUTTER_LIBRARY ${FLUTTER_LIBRARY} PARENT_SCOPE)
set(FLUTTER_ICU_DATA_FILE "${EPHEMERAL_DIR}/icudtl.dat" PARENT_SCOPE)
set(PROJECT_BUILD_DIR "${PROJECT_DIR}/build/" PARENT_SCOPE)
set(AOT_LIBRARY "${PROJECT_DIR}/build/lib/libapp.so" PARENT_SCOPE)

add_library(flutter INTERFACE)
target_include_directories(flutter INTERFACE
  "${EPHEMERAL_DIR}"
)
target_link_libraries(flutter INTERFACE "${FLUTTER_LIBRARY}")
target_link_libraries(flutter INTERFACE
  PkgConfig::GTK
  PkgConfig::GLIB
  PkgConfig::GIO
)

target_sources(flutter INTERFACE
  ${FLUTTER_LIBRARY_HEADERS}
)

add_dependencies(flutter flutter_assemble)

# === Flutter tool backend ===
# _phony_ is a non-existent file to force this command to run every time,
# since currently there's no way to get a full input/output list from the
# flutter tool.
add_custom_command(
  OUTPUT ${FLUTTER_LIBRARY} ${FLUTTER_LIBRARY_HEADERS}
    ${CMAKE_CURRENT_BINARY_DIR}/_phony_
  COMMAND ${CMAKE_COMMAND} -E env
    ${FLUTTER_TOOL_ENVIRONMENT}
    "${FLUTTER_ROOT}/packages/flutter_tools/bin/tool_backend.sh"
      ${FLUTTER_TARGET_PLATFORM} ${CMAKE_BUILD_TYPE}
  VERBATIM
)
add_custom_target(flutter_assemble DEPENDS
  "${FLUTTER_LIBRARY}"
  ${FLUT
