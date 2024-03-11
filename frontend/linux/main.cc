#include "my_application.h"

// Create a new instance of MyApplication using the g_autoptr() convenience wrapper.
// This ensures that the memory allocated for the app will be automatically freed when it goes out of scope.
g_autoptr(MyApplication) app = my_application_new();

// Call the g_application_run() function to start the application's event loop and execute its main() function.
// The function will not return until the application has been terminated.
// The argc and argv arguments are passed directly to the underlying GApplication's main() function.
return g_application_run(G_APPLICATION(app), argc, argv);

