import 'package:flutter/material.dart';
import 'package:auto_gpt_flutter_client/constants/app_colors.dart';

// LoadingIndicator widget displays an animated loading indicator
class LoadingIndicator extends StatefulWidget {
  // Constructor for LoadingIndicator widget
  const LoadingIndicator({Key? key, required this.isLoading}) : super(key: key);

  // A boolean value indicating whether the loading indicator is active or not
  final bool isLoading;

  @override
  _LoadingIndicatorState createState() => _LoadingIndicatorState();
}

// State class for LoadingIndicator widget
class _LoadingIndicatorState extends State<LoadingIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController; // Animation controller for the loading indicator animation
  late Animation<double> _animation; // Animation for the loading indicator

  @override
  void initState() {
    super.initState();

    // Initialize the animation controller with a duration of 2 seconds and vsync set to this
    _animationController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(); // Set the animation to repeat indefinitely

    // Initialize the animation with a tween from 0 to 1
    _animation = Tween<double>(begin: 0, end: 1).animate(_animationController);
  }

  @override
  void dispose() {
    // Dispose the animation controller when the widget is removed from the tree
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width - 65; // Calculate the width of the loading indicator
    width = width > 850 ? 850 : width; // Limit the width to 850 pixels

    return SizedBox(
      width: width, // Set the width of the loading indicator container
      height: 4.0, // Set the height of the loading indicator container
      child: AnimatedBuilder(
        // AnimatedBuilder widget rebuilds when the animation controller changes
        animation: _animationController,
        builder: (context, child) {
          return widget.isLoading // Check if the loading indicator is active
              ? ShaderMask(
                  // ShaderMask widget applies a gradient to the child widget
                  shaderCallback: (rect) {
                    return LinearGradient(
                      // LinearGradient widget creates a gradient with the specified colors and stops
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                      colors: [
                        Colors.grey[400]!, // First color of the gradient
                        AppColors.primaryLight, // Second color of the gradient
                        Colors.white, // Third color of the gradient
                        Colors.grey[400]!, // Fourth color of the gradient
                      ],
                      stops: [
                        _animation.value - 0.5, // First stop of the gradient
                        _animation.value - 0.25, // Second stop of the gradient
                        _animation.value, // Third stop of the gradient
                        _animation.value + 0.25, // Fourth stop of the gradient
                      ],
                    ).createShader(rect);
                  },
                  child: Container(
                    width: width, // Set the width of the container
                    height: 4.0, // Set the height of the container
                    color: Colors.white, // Set the background color of the container
                  ),
                )
              : Container(
                  color: Colors.grey[400], // Set the background color of the container when the loading indicator
