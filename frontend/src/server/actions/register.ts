"use server"

import { redirect } from "next/navigation"
import { z } from "zod"

import { registerFormSchema } from "@/schemas/register"
import { env } from "@/data/env/server"

export async function registerUser(
    { chatId, unsafeData }: {
        chatId: string | null,
        unsafeData: z.infer<typeof registerFormSchema>
    }
): Promise<{ status: boolean; message: string } | undefined> {
    if (!chatId) {
        return {
            status: false,
            message: "We are facing an issue at this time, please contact the owner of the Telegram Bot."
        }
    }
    const { success, data } = registerFormSchema.safeParse(unsafeData)
    if (!success) {
        return { status: false, message: "Facing issue parsing the form data, please contact the owner of the Telegram Bot." }
    }
    const response = await fetch(`${env.SERVER_URL}/api/v0/user/register`, {
        method: "POST",
        body: JSON.stringify({ ...data, chatId: chatId }),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${env.SERVER_API_KEY}`,
        }
    })
    let responseData: { status: boolean, message: string } = await response.json()
    redirect(`/thank-you?status=${responseData.status}&message=${responseData.message}`)
}
