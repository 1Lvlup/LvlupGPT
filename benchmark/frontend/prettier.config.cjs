// Importing Prettier's config type from the 'prettier' module
const { Config } = require("prettier");

// Creating a Prettier config object and setting its plugins property to an array
// that includes the 'prettier-plugin-tailwindcss' module
const config: Config = {
  plugins: [require("prettier-plugin-tailwindcss")],
};

// Exporting the config object as the default export of this module
module.exports = config;
