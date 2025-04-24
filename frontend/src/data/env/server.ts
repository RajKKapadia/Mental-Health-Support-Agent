import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod"

export const env = createEnv({
    emptyStringAsUndefined: true,
    server: {
        SERVER_URL: z.string(),
        SERVER_API_KEY: z.string(),
    },
    experimental__runtimeEnv: process.env
})
