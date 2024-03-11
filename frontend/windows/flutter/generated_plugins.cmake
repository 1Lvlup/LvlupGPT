# Generated file, do not edit.

list(APPEND FLUTTER_PLUGIN_LIST
  firebase_core
  url_launcher_windows
)

list(APPEND FLUTTER_FFI_PLUGIN_LIST
)

set(PLUGIN_BUNDLED_LIBRARIES)

foreach(plugin ${FLUTTER_PLUGIN_LIST})
  add_subdirectory(flutter/ephemeral/.plugin_symlinks/${plugin}/windows plugins/${plugin})
  target_link_libraries(${BINARY_NAME} PRIVATE ${plugin}_plugin)
  list(APPEND PLUGIN_BUNDLED_LIBRARIES $<TARGET_FILE:${plugin}_plugin>)
  
  # Include bundled libraries for the plugin
  foreach(lib ${${plugin}_bundled_libraries})
    list(APPEND PLUGIN_BUNDLED_LIBRARIES ${lib})
  endforeach()
endforeach(plugin)

foreach(ffi_plugin ${FLUTTER_FFI_PLUGIN_LIST})
  add_subdirectory(flutter/ephemeral/.plugin_symlinks/${ffi_plugin}/windows plugins/${ffi_plugin})
  
  # Include bundled libraries for the FFI plugin
  foreach(lib ${${ffi_plugin}_bundled_libraries})
    list(APPEND PLUGIN_BUNDLED_LIBRARIES ${lib})
  endforeach()
endforeach(ffi_plugin)

# Print the list of bundled libraries for debugging purposes
message(STATUS "Bundled libraries: ${PLUGIN_BUNDLED_LIBRARIES}")
