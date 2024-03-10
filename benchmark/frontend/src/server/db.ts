import { PrismaClient } from "@prisma/client";
import { type Env, env } from "~/env.mjs";

let prisma: PrismaClient;

if (process.env.NODE_ENV === "production") {
  prisma = new PrismaClient();
} else {
  if (!globalThis.prisma) {
    globalThis.prisma = new PrismaClient();
  }
  prisma = globalThis.prisma;
  prisma.$use(async (params, next) => {
    // Log all queries in development mode
    if (env.NODE_ENV === "development") {
      console.log("Query: ", params.model, params.action, params.args);
    }
    return next(params);
  });
}

export default prisma;
