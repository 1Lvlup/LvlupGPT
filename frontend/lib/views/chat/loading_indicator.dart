import 'package:flutter/material.dart';
import 'package:auto_gpt_flutter_client/constants/app_colors.dart';

class LoadingIndicator extends StatefulWidget {
  final bool isLoading;

  const LoadingIndicator({Key? key, required this.isLoading}) : super(key: key);

  @override
  _LoadingIndicatorState createState() => _LoadingIndicatorState();
}

class _LoadingIndicatorState extends State<LoadingIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();

    _animationController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat();

    _animation = Tween<double>(begin: 0, end: 1).animate(_animationController);
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width - 65;
    width = width > 850 ? 850 : width;

    return SizedBox(
      width: width,
      height: 4.0,
      child: AnimatedBuilder(
        animation: _animationController,
        builder: (context, child) {
          return widget.isLoading
              ? ShaderMask(
                  shaderCallback: (rect) {
                    return LinearGradient(
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                      colors: [
                        Colors.grey[400]!,
                        AppColors.primaryLight,
                        Colors.white,
                        Colors.grey[400]!,
                      ],
                      stops: [
                        _animation.value - 0.5,
                        _animation.value - 0.25,
                        _animation.value,
                        _animation.value + 0.25,
                      ],
                    ).createShader(rect);
                  },
                  child: Container(
                    width: width,
                    height: 4.0,
                    color: Colors.white,
                  ),
                )
              : Container(
                  color: Colors.grey[400],
                );
        },
      ),
    );
  }
}
