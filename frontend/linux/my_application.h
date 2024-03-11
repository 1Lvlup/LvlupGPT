#ifndef FLUTTER_MY_APPLICATION_H_
#define FLUTTER_MY_APPLICATION_H_

#include <gtk/gtk.h>
#include <flutter/flutter.h>

G_DECLARE_FINAL_TYPE(MyApplication, my_application, MY, APPLICATION,
                     GtkApplication)

struct _MyApplication {
  GtkApplication parent_instance;
  FlutterDesktopEngine *flutter_engine;
};

G_DEFINE_TYPE(MyApplication, my_application, GTK_TYPE_APPLICATION)

MyApplication *
my_application_new(void) {
  return g_object_new(my_application_get_type(),
                       "application-id", "com.example.my_application",
                       "flags", G_APPLICATION_FLAGS_NONE,
                       NULL);
}

static void
my_application_activate(GApplication *application) {
  MyApplication *my_app = MY_APPLICATION(application);
  GtkWidget *window;

  window = gtk_application_window_new(my_app);
  gtk_window_set_title(GTK_WINDOW(window), "My Flutter Application");
  gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);

  if (my_app->flutter_engine == NULL) {
    my_app->flutter_engine = flutter_desktop_engine_new(gtk_widget_get_drawing_area(GTK_WINDOW(window)));
  }

  gtk_widget_show_all(window);
}

static void
my_application_startup(GApplication *application) {
  G_APPLICATION_CLASS(my_application_parent_class)->startup(application);

  my
