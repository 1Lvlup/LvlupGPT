import { PrismaClient } from "@prisma/client";
import { type Env, env } from "~/env.mjs"; // Import the env object for accessing the NODE_ENV value

let prisma: PrismaClient; // Declare a variable to store the Prisma Client instance

if (process.env.NODE_ENV === "production") { // Check if the application is running in the production environment
  prisma = new PrismaClient(); // Create a new Prisma Client instance
} else {
  if (!globalThis.prisma) { // Check if a global Prisma Client instance already exists
    globalThis.prisma = new PrismaClient(); // Create a new Prisma Client instance and store it in the globalThis object
  }
  prisma = globalThis.prisma; // Assign the existing or new Prisma Client instance to the local prisma variable

  prisma.$use(async (params, next) => { // Add a middleware to log all queries in non-production environments
    // Log all queries in development mode
    if (env.NODE_ENV === "development") {
      console.log("Query: ", params.model, params.action, params.args);
    }
    return next(params); // Proceed with the original query
  });
}

export
