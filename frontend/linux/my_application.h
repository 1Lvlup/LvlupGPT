// Include necessary headers for the GTK and Flutter libraries.
#include <gtk/gtk.h>
#include <flutter/flutter.h>

// Declare a new final type for the MyApplication struct, which inherits from GtkApplication.
G_DECLARE_FINAL_TYPE(MyApplication, my_application, MY, APPLICATION, GtkApplication)

// Define the MyApplication struct, which contains a GtkApplication parent_instance and a FlutterDesktopEngine flutter_engine.
struct _MyApplication {
  GtkApplication parent_instance;
  FlutterDesktopEngine *flutter_engine;
};

// Define the type for MyApplication as inheriting from GtkApplication.
G_DEFINE_TYPE(MyApplication, my_application, GTK_TYPE_APPLICATION)

// Create a new instance of MyApplication, setting the application ID, flags, and passing NULL for additional parameters.
MyApplication *
my_application_new(void) {
  return g_object_new(my_application_get_type(),
                       "application-id", "com.example.my_application",
                       "flags", G_APPLICATION_FLAGS_NONE,
                       NULL);
}

// Callback function for when the application is activated.
// This creates a new GtkWindow, sets its title and default size, and displays it.
// If the flutter_engine is not yet initialized, it is created and associated with the drawing area of the window.
static void
my_application_activate(GApplication *application) {
  MyApplication *my_app = MY_APPLICATION(application);
  GtkWidget *window;

  window = gtk_application_window_new(my_app);
  gtk_window_set_title(GTK_WINDOW(window), "My Flutter Application");
  gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);

  if (my_app->flutter_engine == NULL) {
    my_app->flutter_engine = flutter_desktop_engine_new(gtk_widget_get_drawing_
