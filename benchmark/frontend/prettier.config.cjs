// Importing Prettier's config type
const { Config } = require("prettier");

// Creating the Prettier config object
const config: Config = {
  plugins: [require("prettier-plugin-tailwindcss")],
};

// Exporting the config object
module.exports = config;
