import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart'; // Importing SettingsViewModel
import 'package:flutter/material.dart'; // Importing Material Design widgets
import 'package:provider/provider.dart'; // Importing Provider for state management

class ApiBaseUrlField extends StatelessWidget {
  // Creating a stateless widget for the API base URL input field
  final TextEditingController controller = TextEditingController(); // Creating a TextEditingController for the input field

  @override
  Widget build(BuildContext context) {
    return Consumer<SettingsViewModel>( // Using Consumer to access SettingsViewModel
      builder: (context, settingsViewModel, child) {
        // TODO: This view shouldn't know about the settings view model. It should use a delegate
        controller.text = settingsViewModel.baseURL; // Setting the initial value of the input field to the current base URL

        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16), // Adding horizontal padding to the container
          child: Column(
            children: [
              Container(
                height: 50, // Setting the height of the input field container
                decoration: BoxDecoration(
                  color: Colors.white, // Setting the background color of the input field container
                  border: Border.all(color: Colors.black, width: 0.5), // Adding a border to the input field container
                  borderRadius: BorderRadius.circular(8), // Setting the border radius of the input field container
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8), // Adding horizontal padding to the input field
                  child: TextField(
                    controller: controller, // Assigning the TextEditingController to the input field
                    decoration: const InputDecoration(
                      border: InputBorder.none, // Removing the default border of the input field
                      hintText: 'Agent Base URL', // Adding a hint text to the input field
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16), // Adding vertical spacing between the input field and the buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly, // Horizontally centering the buttons
                children: [
                  ElevatedButton(
                    onPressed: () {
                      controller.text = 'http://127.0.0.1:8000/ap/v1'; // Setting the input field value to the default URL
                      settingsViewModel.updateBaseURL(controller.text); // Updating the base URL in the SettingsViewModel
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white, // Setting the background color of the button
                      foregroundColor: Colors.black, // Setting the text color of the button
                      textStyle: const TextStyle(
                        color: Colors.black, // Setting the text color of the button
                      ),
                    ),
                    child: const Text("Reset"), // Adding the "Reset" label to the button
                  ),
                  ElevatedButton(
                    onPressed: () {
                      settingsViewModel.updateBaseURL(controller.text); // Updating the base URL in the SettingsViewModel
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white, // Setting the background color of the button
                      foregroundColor: Colors.black, // Setting the text color of the button
                      textStyle: const TextStyle(
                        color: Colors.black, // Setting the text color of the button
                      ),
                    ),
                    child: const Text("Update"), // Adding the "Update" label to the button
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}

