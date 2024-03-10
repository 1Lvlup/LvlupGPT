import { createEnv, type Env } from "@t3-oss/env-nextjs";
import { z } from "zod";

const serverEnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]),
});

const clientEnvSchema = z.object({
  NEXT_PUBLIC_CLIENTVAR: z.string().min(1),
});

const runtimeEnvSchema = z.object({
  NODE_ENV: z.string(),
  NEXT_PUBLIC_CLIENTVAR: z.string(),
});

export const env: Env = createEnv({
  server: serverEnvSchema,
  client: clientEnvSchema.omit({ NEXT_PUBLIC_CLIENTVAR: true }).extend({
    NEXT_PUBLIC_ANOTHER_VAR: z.string().min(1),
  }),
  runtimeEnv: runtimeEnvSchema,
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
});

// Validate the env vars before accessing them
env.parse();

// Now you can safely access the env vars
const nodeEnv = env.NEXT_PUBLIC_CLIENTVAR;
const clientVar = env.NEXT_PUBLIC_CLIENTVAR;
const anotherVar = env.NEXT_PUBLIC_ANOTHER_VAR;
