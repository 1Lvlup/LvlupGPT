#!/bin/bash

# Check if Flutter is installed
if ! command -v flutter &> /dev/null
then
    echo "Flutter is not installed. Please install Flutter before running this script."
    exit 1
fi

# Check if the current working directory is a Flutter project
if [ ! -d ios ] || [ ! -d android ] || [ ! -d linux ] || [ ! -d windows ] || [ ! -d web ] || [ ! -f pubspec.yaml ]; then
    echo "This does not appear to be a Flutter project directory. Please run this script from the root directory of your Flutter project."
    exit 1
fi

# Build the web version of the Flutter app
echo "Building web version of the Flutter app..."
flutter build web --base-href /app/

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Failed to build the web version of the Flutter app. Please check the console for errors."
    exit 1
fi

echo "Web version of the Flutter app has been built successfully."
