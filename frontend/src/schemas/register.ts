import { z } from "zod"

export const registerFormSchema = z.object({
    firstName: z.string().min(2, { message: "First name must be at least 2 characters" }),
    lastName: z.string().min(2, { message: "Last name must be at least 2 characters" }),
    email: z.string().email({ message: "Please enter a valid email address" }),
    age: z.coerce
        .number()
        .min(18, { message: "You must be at least 18 years old" })
        .max(120, { message: "Please enter a valid age" }),
    gender: z.string().min(1, { message: "Please select a gender" }),
    privacyPolicy: z.boolean().refine((val) => val === true, {
        message: "You must accept the privacy policy",
    }),
})

export type RegisterSchema = z.infer<typeof registerFormSchema>
