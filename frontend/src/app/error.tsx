"use client"

import { useEffect } from "react"

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error(error)
    }, [error])

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
            <div className="max-w-lg w-full text-center">
                <div className="mb-6">
                    <div className="relative inline-block">
                        <div className="w-24 h-24 rounded-full bg-red-100 flex items-center justify-center">
                            <svg className="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                            </svg>
                        </div>
                    </div>
                </div>

                <h2 className="text-2xl font-bold text-gray-800 mb-3">Something went wrong!</h2>

                <p className="text-gray-600 mb-8">
                    We apologize for the inconvenience. An unexpected error has occurred.
                    {process.env.NODE_ENV === "development" && (
                        <div className="mt-4 p-4 bg-gray-100 rounded-md text-left">
                            <p className="text-sm font-mono text-red-600 break-words">
                                {error.message || "Unknown error occurred"}
                            </p>
                        </div>
                    )}
                </p>
            </div>
        </div>
    )
}