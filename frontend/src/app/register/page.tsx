"use client"

import { useSearchParams } from "next/navigation"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { useState } from "react"
import { registerFormSchema, RegisterSchema } from "@/schemas/register"
import { registerUser } from "@/server/actions/register"

export default function UserInfoForm() {
    const searchParams = useSearchParams()
    const chatId = searchParams.get("chatId")
    const [errorMessage, setErrorMessage] = useState<string | null>(null)

    const form = useForm<RegisterSchema>({
        resolver: zodResolver(registerFormSchema),
        defaultValues: {
            firstName: "Raj",
            lastName: "Kapadia",
            email: "raajforyou@gmail.com",
            age: 25,
            gender: "Male",
            privacyPolicy: true,
        },
    })

    const onSubmit = async (formData: RegisterSchema) => {
        console.log("Form Data:", formData)
        console.log("Chat ID:", chatId)
        const data = await registerUser({ chatId: chatId, unsafeData: formData })
        if (!data?.status) {
            setErrorMessage(data?.message!)
        }
    }

    if (!chatId) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="flex flex-col items-center">
                    <div className="relative">
                        <div className="w-16 h-16 border-4 border-gray-200 rounded-full animate-spin border-t-gray-900"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-8 h-8 bg-gray-500 rounded-full animate-pulse opacity-70"></div>
                        </div>
                    </div>

                    <p className="mt-4 text-xl font-medium text-gray-900">Loading...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="container mx-auto py-10 px-4">
            {
                errorMessage && (
                    <div className="flex items-center, justify-center mb-6">
                        <p className="text-sm font-mono text-red-600 break-words">
                            {errorMessage}
                        </p>
                    </div>
                )
            }
            <Card className="max-w-lg mx-auto">
                <CardHeader>
                    <CardTitle>User Information</CardTitle>
                    <CardDescription>
                        Please fill out the form below to complete your profile.
                        {chatId && <span className="block text-sm mt-1">Chat ID: {chatId}</span>}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="firstName"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>First Name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="John" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="lastName"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Last Name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Doe" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="email"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Email</FormLabel>
                                        <FormControl>
                                            <Input type="email" placeholder="john.doe@example.com" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="age"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Age</FormLabel>
                                            <FormControl>
                                                <Input
                                                    type="number"
                                                    placeholder="25"
                                                    {...field}
                                                    onChange={(e) => {
                                                        field.onChange(e.target.value === "" ? undefined : Number.parseInt(e.target.value, 10))
                                                    }}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="gender"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Gender</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select gender" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent defaultValue={"Male"}>
                                                    <SelectItem value="Male">Male</SelectItem>
                                                    <SelectItem value="Female">Female</SelectItem>
                                                    <SelectItem value="Other">Other</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="privacyPolicy"
                                render={({ field }) => (
                                    <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
                                        <FormControl>
                                            <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                                        </FormControl>
                                        <div className="space-y-1 leading-none">
                                            <FormLabel>Privacy Policy</FormLabel>
                                            <FormDescription>I agree to the privacy policy and terms of service.</FormDescription>
                                        </div>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <Button type="submit" className="w-full">
                                Submit
                            </Button>
                        </form>
                    </Form>
                </CardContent>
            </Card>
        </div>
    )
}
