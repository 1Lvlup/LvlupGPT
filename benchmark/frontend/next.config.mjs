/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */

// Import the environment variables and validate them
import "./src/env.mjs";

/**
 * The Next.js configuration object.
 * @type {import("next").NextConfig}
 */
const nextConfig = {
  // Enable strict mode for React components
  reactStrictMode: true,

  /**
   * Internationalization configuration.
   *
   * Note: If you are using `appDir`, you must comment out the below `i18n` config.
   *
   * @see https://github.com/vercel/next.js/issues/41980
   */
  i18n: {
    // List of supported locales
    locales: ["en"],
    // Default locale for the application
    defaultLocale: "en",
  },
};

// Export the Next.js configuration object
module.exports = nextConfig;
