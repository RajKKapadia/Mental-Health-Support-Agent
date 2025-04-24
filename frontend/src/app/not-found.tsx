import React from 'react'

export default function NotFound() {
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <div className="text-center px-4">
                <div className="mb-8">
                    <h1 className="text-9xl font-bold text-gray-200">404</h1>
                </div>

                <h2 className="text-2xl font-semibold text-gray-800 mb-3">Page Not Found</h2>
                <p className="text-gray-600 mb-8">
                    The page you are looking for doesn't exist or has been moved. You have landed here by mistake.
                </p>
                <p className="text-gray-600 mb-8 font-semibold text-xl">
                    You can close this window.
                </p>
            </div>
        </div>
    )
}
