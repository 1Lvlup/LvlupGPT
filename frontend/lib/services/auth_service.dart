import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';

/// The main AuthService class that handles user authentication using
/// Firebase Authentication and Google/GitHub sign-in providers.
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance; // Firebase Authentication instance
  final GoogleSignIn googleSignIn = GoogleSignIn(
      clientId:  // Google Sign-In client ID
          "387936576242-iejdacrjljds7hf99q0p6eqna8rju3sb.apps.googleusercontent.com");

  /// Sign in with Google using redirect.
  ///
  /// This method initiates the Google Sign-In process using the GoogleSignIn
  /// instance and Firebase Authentication to sign in the user.
  ///
  /// Returns a Future that resolves to a UserCredential object if the sign-in
  /// is successful, or null if there is an error.
  Future<UserCredential?> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? googleSignInAccount =
          await googleSignIn.signIn(); // Sign in with Google using GoogleSignIn instance
      if (googleSignInAccount != null) {
        final GoogleSignInAuthentication googleSignInAuthentication =
            await googleSignInAccount.authentication; // Get Google Sign-In authentication details
        final AuthCredential credential = GoogleAuthProvider.credential(
          accessToken: googleSignInAuthentication.accessToken, // Create a Firebase AuthCredential using the Google authentication details
          idToken: googleSignInAuthentication.idToken,
        );
        return await _auth.signInWithCredential(credential); // Sign in with Firebase Authentication using the AuthCredential
      }
    } catch (e) {
      print("Error during Google Sign-In: $e"); // Print the error if there is one
      return null;
    }
  }

  /// Sign in with GitHub using redirect.
  ///
  /// This method initiates the GitHub Sign-In process using Firebase Authentication
  /// and returns a Future that resolves to a UserCredential object if the sign-in
  /// is successful, or null if there is an error.
  Future<UserCredential?> signInWithGitHub() async {
    try {
      final GithubAuthProvider provider = GithubAuthProvider(); // Create a GithubAuthProvider instance
      return await _auth.signInWithPopup(provider); // Sign in with Firebase Authentication using the G
