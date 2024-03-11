// Include the necessary headers for the application, including the custom
// "my_application.h" header, the Flutter Linux header, and GTK headers.
#include "my_application.h"
#include <flutter_linux/flutter_linux.h>
#ifdef GDK_WINDOWING_X11
#include <gdk/gdkx.h>
#endif
#include <gtk/gtk.h>
#include <flutter/generated_plugin_registrant.h>

// Define the structure for the custom MyApplication type, which inherits from
// GtkApplication. This structure contains a pointer to the parent instance
// and an array of dart_entrypoint_arguments.
struct _MyApplication {
  GtkApplication parent_instance;
  char** dart_entrypoint_arguments;
};

// Register the custom MyApplication type with GObject.
G_DEFINE_TYPE(MyApplication, my_application, GTK_TYPE_APPLICATION)

// The my_application_activate function is called when the application is
// activated. It creates a new GTK window, sets the title and default size,
// and shows the window. It also creates a new FlDartProject instance, sets
// the dart_entrypoint_arguments, and creates a new FlView instance. The FlView
// instance is added to the window and the plugins are registered.
static void my_application_activate(GApplication* application) {
  MyApplication* self = MY_APPLICATION(application);
  GtkWindow* window = GTK_WINDOW(gtk_application_window_new(GTK_APPLICATION(application)));

  // ... rest of the function implementation ...
}

// The my_application_local_command_line function is called when the application
// is started from the command line. It processes the command line arguments,
// registers the application, and activates the application.
static gboolean my_application_local_command_line(GApplication* application, gchar*** arguments, int* exit_status) {
  g_return_if_fail(application != NULL);
  g_return_if_fail(arguments != NULL);
  g_return_if_fail(exit_status != NULL);

  MyApplication* self = MY_APPLICATION(application);
  self->dart_entrypoint_arguments = g_autofree char** = g_steal_pointer(&arguments[1]);

  // ... rest of the function implementation ...
}

// The my_application_dispose function is called when the custom MyApplication
// object is being destroyed. It clears the dart_entrypoint_arguments pointer.
static void my_application_dispose(GObject* object) {
  MyApplication* self = MY_APPLICATION(object);
  g_clear_pointer(&self->dart_entrypoint_arguments, g_strfreev);
  G_OBJECT_CLASS(my_application_parent_class)->dispose(object);
}

// The my_application_class_init function initializes the custom MyApplication
// class. It sets the activate, local_command_line, and dispose class functions.
static void my_application_class_init(MyApplicationClass* klass) {
  G_APPLICATION_CLASS(klass)->activate = my_application_activate;
  G_APPLICATION_CLASS(klass)->local_command_line = my_application_local_command_line;
  G_OBJECT_CLASS(klass)->dispose = my_application_dispose;
}

// The my_application_init function initializes the custom MyApplication instance.
static void my_application_init(MyApplication* self) {}

// The my_application_new function creates a new instance of the custom
// MyApplication object.
MyApplication* my_application_new() {
  return MY_APPLICATION(g_object_new(my_application_get_type(),
                                     "application-id", APPLICATION_ID,
                                     "flags", G_APPLICATION_NON_UNIQUE,
                                     nullptr));
}
