import { createEnv } from "@t3-oss/env-nextjs"
import { z } from "zod"

export const env = createEnv({
    emptyStringAsUndefined: true,
    client: {
        NEXT_PUBLIC_SERVER_URL: z.string(),
        NEXT_PUBLIC_SERVER_API_KEY: z.string(),
    },
    experimental__runtimeEnv: {
        NEXT_PUBLIC_SERVER_URL: process.env.NEXT_PUBLIC_SERVER_URL,
        NEXT_PUBLIC_SERVER_API_KEY: process.env.NEXT_PUBLIC_SERVER_API_KEY,
    }
})
