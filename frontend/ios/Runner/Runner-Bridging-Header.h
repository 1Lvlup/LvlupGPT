#import "GeneratedPluginRegistrant.h"

// Import the header file for your Flutter plugin.
#import "MyFlutterPlugin.h"

@implementation FlutterPluginRegistrant

+ (void)registerWithRegistrar:(NSFlutterRegistrar *)registrar {
  // Register your plugin with the Registrar.
  [MyFlutterPlugin registerWithRegistrar:registrar];
}

@end
