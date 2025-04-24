export default async function RegistrationComplete({ searchParams }: { searchParams: Promise<{ status: boolean | null, message: string | null }> }) {

    const { status, message } = await searchParams

    if (status == null || message == null) {
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

    if (status) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
                <div className="max-w-lg w-full text-center p-8 bg-white rounded-xl shadow-lg">
                    <div className="mb-6">
                        <div className="w-20 h-20 mx-auto rounded-full bg-green-100 flex items-center justify-center">
                            <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                    </div>

                    <h1 className="text-3xl font-bold text-gray-800 mb-4">Thank You!</h1>

                    <h2 className="text-xl font-medium text-gray-700 mb-6">{message}</h2>

                    <p className="text-gray-600 mb-8">
                        We"ve successfully processed your registration. You can now close this window.
                    </p>

                    <div className="border-t border-gray-200 pt-6">
                        <p className="text-sm text-gray-500">
                            You can start interacting with the Telegram Bot.
                        </p>
                        <p className="text-gray-600 mb-8 font-semibold text-xl">
                            You can close this window.
                        </p>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
            <div className="max-w-lg w-full text-center p-8 bg-white rounded-xl shadow-lg">
                <div className="mb-6">
                    <div className="w-20 h-20 mx-auto rounded-full bg-green-100 flex items-center justify-center">
                        <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                    </div>
                </div>

                <h1 className="text-3xl font-bold text-gray-800 mb-4">Thank You!</h1>

                <h2 className="text-xl font-medium text-gray-700 mb-6">{message}</h2>

                <p className="text-gray-600 mb-8">
                    We are unable to perform the registration process.
                </p>

                <div className="border-t border-gray-200 pt-6">
                    <p className="text-gray-600 mb-8 font-semibold text-xl">
                        You can close this window.
                    </p>
                </div>
            </div>
        </div>
    )
}